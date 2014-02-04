This works with Python 2.7.6 and since Heroku defaults to this version there is no runtime.txt to declare a version. There is also no Procfile because this only installs the program on Heroku and makes it availabe from the command line. 

I'm using this to scrap emails and reply to them. I'm not a spammer and you should NOT CLONE THIS if you intent to use it for spam. I simply want to show potential employers that I can reach out to them automatically. 

I ~~m trying to get~~ got this working on Heroku and found this https://github.com/thnkr/cloak. It's a really cool tool and I'll adapt what I learned from it in later work, unfortunately it doesn't work for this use-case. ~~Hunting for~~ Found the answer. :)

Refer to [middleware.py](https://github.com/MrRyanAlexander/Mad_Bot/blob/master/mad_bot/middleware.py "Middleware.PY") for changing the proxy.

Some quick commands:

  The really cool streaming Heroku log

  ```
  heroku logs --tail 

  ```
  Run any scraper manually; launches a streaming log view too

  ```
  heroku run scrapy crawl [crawler_name]

  ```

To deploy jobs using the Heroky Scheduler, simply create a job by entering: $ scray crawl [crawler_name] then set times and save

If you want to reuse the storage method I used here, you will need to create an app on Parse.com and add your API keys in the settings.py file

Finally, if you choose Parse, you'll need to create cloud functions like below, or just copy and reuse these :)
  ```
  var Scrape = Parse.Object.extend("Scrape");
  Parse.Cloud.beforeSave("Scrape", function(request, response) {
    if (!request.object.get("scrapeID")) {
      response.error('A Scrape must have an id.');
    } else {
      var query = new Parse.Query(Scrape);
      query.equalTo("scrapeID", request.object.get("scrapeID"));
      query.first({
        success: function(object) {
          if (object) {
            response.error("A Scrape with this id already exists.");
          } else {
            response.success();
          }
        },
        error: function(error) {
          response.error("Could not validate uniqueness for this Scrape object.");
        }
      });
    }
  });
  
  Parse.Cloud.define("scrapeSaver", function(req, res) {
      Parse.Cloud.useMasterKey();
      var email = req.params.email;
      var referer = req.params.referer;
      var id = req.params.scrapeID;
      var scrape = new Scrape();
      scrape.set("email", email);
      scrape.set("referer", referer);
      scrape.set("scrapeID", id);
      scrape.save(null, {
          success: function() {
              res.success("Success!");
          },
          error: function(s, e) {
              res.error("Failure :" + JSON.stringify(e));
          }
      });
  });
  ```
If you have any question, concerns, complaints or requests; issue a pull request and I will respond. 
