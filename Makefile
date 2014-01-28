PY                  = python

IR_ITERS            = 3
IR_PARAMS           = -t 0 -c 2.0 -h 0
RW_ALPHA            = 0.1
RW_AXIS             = 1

SRC_PATH            = ./src
DATA_PATH           = ./data

MAIN_SCRIPT_PATH    = $(SRC_PATH)/main.py

RAW_DATA_PATH       = $(DATA_PATH)/raw
GRAPH_DATA_PATH     = $(DATA_PATH)/graph
SEED_DATA_PATH      = $(DATA_PATH)/seeds
IR_DATA_PATH        = $(DATA_PATH)/iterreg
RW_DATA_PATH        = $(DATA_PATH)/randwalk
CERT_DATA_PATH      = $(DATA_PATH)/certainty
TRUTH_DATA_PATH     = $(DATA_PATH)/truth

RAW_CN5_PATH        = $(RAW_DATA_PATH)/conceptnet5/conceptnet4_[0-4].csv
RAW_ANEW_PATH       = $(RAW_DATA_PATH)/anew.csv
RAW_SN_PATH         = $(RAW_DATA_PATH)/senticnet.rdf.xml

ANEW_PATH           = $(SEED_DATA_PATH)/anew.txt
SN_PATH             = $(SEED_DATA_PATH)/sn.txt

NODES_PATH          = $(GRAPH_DATA_PATH)/nodes.txt
EDGES_PATH          = $(GRAPH_DATA_PATH)/edges.txt
RELS_PATH           = $(GRAPH_DATA_PATH)/rels.txt

IR_PRED_PATH_TMPL   = $(IR_DATA_PATH)/r[i].txt
IR_PRED_PATHS       = $(subst [i],[1-$(IR_ITERS)],$(IR_PRED_PATH_TMPL))

RW_PRED_PATH        = $(RW_DATA_PATH)/r1.txt

IR_CERT_PATH        = $(CERT_DATA_PATH)/iterreg.txt
RW_CERT_PATH        = $(CERT_DATA_PATH)/randwalk.txt
IMPACT_PATH         = $(CERT_DATA_PATH)/impact.txt

POL_TRUTH_1_PATH    = $(TRUTH_DATA_PATH)/1.txt
POL_TRUTH_2_PATH    = $(TRUTH_DATA_PATH)/2.txt
RANK_TRUTH_1_PATH   = $(TRUTH_DATA_PATH)/pairs1.txt
RANK_TRUTH_2_PATH   = $(TRUTH_DATA_PATH)/pairs2.txt

# $(call eval-pred,metric,pred,truth)
define eval-pred
	$(PY) $(MAIN_SCRIPT_PATH) eval $1 --pred $2 --truth $3
endef

# $(call eval-pred-all,title,pred)
define eval-pred-all
	echo [$1] \
	    Polarity Accuracy = \
	    `$(call eval-pred,polarity,$2,$(POL_TRUTH_1_PATH))` \
	    `$(call eval-pred,polarity,$2,$(POL_TRUTH_2_PATH))` \
	    Kendall-Tau = \
	    `$(call eval-pred,kendall,$2,$(RANK_TRUTH_1_PATH))` \
	    `$(call eval-pred,kendall,$2,$(RANK_TRUTH_2_PATH))`
endef

.PHONY: split seeds seeds-anew seeds-sn iterreg iterreg-certainty randwalk shift \
	impact \
	lookup eval eval-sn eval-iterreg eval-randwalk \
	clean clean-graph clean-seeds clean-iterreg clean-randwalk clean-certainty

all: split seeds iterreg iterreg-certainty randwalk shift

split:
	@echo "Parsing ConceptNet..."
	@mkdir -p $(GRAPH_DATA_PATH)
	@$(PY) $(MAIN_SCRIPT_PATH) split \
	    --graph $(RAW_CN5_PATH) \
	    --nodes $(NODES_PATH) \
	    --edges $(EDGES_PATH) \
	    --rels  $(RELS_PATH)

seeds: seeds-anew seeds-sn

seeds-anew:
	@echo "Parsing ANEW..."
	@mkdir -p $(SEED_DATA_PATH)
	@$(PY) $(MAIN_SCRIPT_PATH) seeds anew \
	    --raw   $(RAW_ANEW_PATH) \
	    --seed  $(ANEW_PATH) \
	    --nodes $(NODES_PATH)

seeds-sn:
	@echo "Parsing SenticNet..."
	@mkdir -p $(SEED_DATA_PATH)
	@$(PY) $(MAIN_SCRIPT_PATH) seeds sn \
	    --raw   $(RAW_SN_PATH) \
	    --seed  $(SN_PATH) \
	    --nodes $(NODES_PATH)

iterreg:
	@echo "Performing iterative regression..."
	@mkdir -p $(IR_DATA_PATH)
	@$(PY) $(MAIN_SCRIPT_PATH) iterreg \
	    --anew  $(ANEW_PATH) \
	    --sn    $(SN_PATH) \
	    --edges $(EDGES_PATH) \
	    --pred  $(subst [i],1,$(IR_PRED_PATH_TMPL)) \
	    --param "$(IR_PARAMS)"
	@for i in {2..$(IR_ITERS)}; do \
	    $(PY) $(MAIN_SCRIPT_PATH) iterreg \
	        --anew  $(ANEW_PATH) \
	        --sn    $(SN_PATH) \
	        --edges $(EDGES_PATH) \
	        --pis   $(subst [i],$$((i - 1)),$(IR_PRED_PATH_TMPL)) \
	        --pred  $(subst [i],$$i,$(IR_PRED_PATH_TMPL)) \
	        --param "$(IR_PARAMS)"; \
	done

iterreg-certainty:
	@echo "Generating certainty scores for iterative regression..."
	@mkdir -p $(CERT_DATA_PATH)
	@$(PY) $(MAIN_SCRIPT_PATH) ircert \
	    --preds $(IR_PRED_PATHS) \
	    --cert  $(IR_CERT_PATH)

randwalk:
	@echo "Performing random walk..."
	@mkdir -p $(RW_DATA_PATH)
	@$(PY) $(MAIN_SCRIPT_PATH) randwalk \
	    --edges     $(EDGES_PATH) \
	    --seed      $(subst [i],$(IR_ITERS),$(IR_PRED_PATH_TMPL)) \
	    --pred      $(RW_PRED_PATH) \
	    --cin       $(IR_CERT_PATH) \
	    --cout      $(RW_CERT_PATH) \
	    --alpha     $(RW_ALPHA) \
	    --axis      $(RW_AXIS)

shift:
	@echo "Shifting..."
	@$(PY) $(MAIN_SCRIPT_PATH) shift mva \
	    --seed      $(ANEW_PATH) \
	    --pred_in   $(RW_PRED_PATH) \
	    --pred_out  $(RW_PRED_PATH)

impact:
	@echo "Calculating impacts..."
	@mkdir -p $(RW_DATA_PATH)
	@$(PY) $(MAIN_SCRIPT_PATH) impact \
	    --edges     $(EDGES_PATH) \
	    --impact    $(IMPACT_PATH) \
	    --alpha     $(RW_ALPHA) \
	    --axis      $(RW_AXIS)

lookup:
	@$(PY) $(MAIN_SCRIPT_PATH) lookup \
	    --nodes     $(NODES_PATH) \
	    --edges     $(EDGES_PATH) \
	    --rels      $(RELS_PATH) \
	    --anew      $(ANEW_PATH) \
	    --sn        $(SN_PATH) \
	    --pred      $(RW_PRED_PATH)

eval: eval-iterreg eval-randwalk

eval-iterreg:
	@echo --- IterReg ---
	@for i in {1..$(IR_ITERS)}; do \
	    $(call eval-pred-all,iter $$i,$(subst [i],$$i,$(IR_PRED_PATH_TMPL))); \
	done

eval-randwalk:
	@echo --- RandWalk ---
	@$(call eval-pred-all,alpha=$(RW_ALPHA),$(RW_PRED_PATH)); \

clean: clean-graph clean-seeds clean-iterreg clean-randwalk clean-certainty

clean-graph:
	$(RM) -r $(GRAPH_DATA_PATH)

clean-seeds:
	$(RM) -r $(SEED_DATA_PATH)

clean-iterreg:
	$(RM) -r $(IR_DATA_PATH)

clean-randwalk:
	$(RM) -r $(RW_DATA_PATH)

clean-certainty:
	$(RM) -r $(CERT_DATA_PATH)
