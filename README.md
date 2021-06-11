# FCC recording upload to Telegram

To schedule this run crontab -e and add below line

```
0 18 * * * cd {project dir} && ./run.sh
```