chcp 65001
python -m litedoc tests/test_modules/mbcp -o docdist/api -l zh-Hans -fd def -md def -cd 类 -cs -bu https://github.com/snowykami/mbcp/tree/main/mbcp/
python -m litedoc tests/test_modules/mbcp -o docdist/en/api -l en -fd def -md def -cs -bu https://github.com/snowykami/mbcp/tree/main/mbcp/