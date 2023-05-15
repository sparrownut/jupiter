rm -rf outs/*
cp getSheet_linux outs
for it in `cat list`
do
	./ENScan -n $it -field icp
done
cd outs
./getSheet_linux
cd ..