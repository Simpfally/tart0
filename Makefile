test:
	@python3 test_all.py

bench:
	@./benchmark > .tempbench
	@head .tempbench
	@rm .tempbench

clean:
	@rm -rfv __pycache__

pdf:
	pandoc README.md -o README.pdf
