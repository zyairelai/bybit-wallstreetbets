heroku git:remote -a long-term-low-leverage
git add .
git commit -m "deploy"
git push heroku master
heroku ps:scale worker=1
