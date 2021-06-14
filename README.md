# FCC recording upload to Telegram

## Generate FCC API key

https://www.freeconferencecall.com/for-developers/free-api


To schedule this run crontab -e and add below line

```
0 18 * * * cd {project dir} && ./run.sh
```