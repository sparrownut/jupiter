echo -e "\e[32m正在清理输出目录...\e[0m"
rm -rf outs/*
echo -e "\e[32m复制 getSheet_linux 到输出目录...\e[0m"
cp getSheet_linux outs

echo -e "\e[34m启动 mitmproxy...\e[0m"
sudo docker run --rm -itd -p 8080:8080 mitmproxy/mitmproxy mitmproxy

echo -e "\e[34m下载 mitmproxy 证书...\e[0m"
curl -x http://localhost:8080 http://mitm.it/cert/pem -o mitmproxy-ca-cert.pem

echo -e "\e[34m安装 mitmproxy 证书...\e[0m"
sudo cp mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy-ca-cert.crt
sudo update-ca-certificates

echo -e "\e[32m删除临时证书文件...\e[0m"
rm -rf mitmproxy-ca-cert.pem

echo -e "\e[33m预热10秒...\e[0m"
sleep 10

echo -e "\e[33m开始运行 ENScan...\e[0m"
for it in `cat list`
do
    echo -e "\e[36m正在处理 $it...\e[0m"
    ./ENScan -n $it -field icp --branch -invest 50 -deep 5 -proxy http://127.0.0.1:8080
done

echo -e "\e[33m生成报告...\e[0m"
cd outs
./getSheet_linux
cat output.txt

echo -e "\e[32m脚本执行完毕！\e[0m"
cd ..