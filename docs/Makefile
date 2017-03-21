.PHONY:all clean show

IN := neccodb.er
OUT := ./out/$(IN:.er=.png)
ERD := ./erd/dist/build/erd/erd

all:show $(ERD)

show:$(OUT)
	@if [ ! -z "$(shell which open)" ]; then \
		open $<; \
	fi

$(OUT):$(IN)
	@$(ERD) -i $(<) -o $(@)
	@echo "all done"

$(ERD):./erd/Makefile
	cd erd
	make

./erd/Makefile:
	git clone git://github.com/BurntSushi/erd

clean:
	rm -f $(OUT)
