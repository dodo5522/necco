IN := neccodb.er
OUT := ./out/$(IN:.er=.png)
ERD := ./erd/dist/build/erd/erd

all:$(OUT) $(ERD)

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
