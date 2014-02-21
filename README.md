This works with Python 2.7.6 and since Heroku defaults to this version there is no runtime.txt to declare a version. There is also no Procfile because this only installs the program on Heroku and makes it availabe from the command line. 

I ~~m trying to get~~ got this working on Heroku and found this https://github.com/thnkr/cloak. It's a really cool tool and I'll adapt what I learned from it in later work, unfortunately it doesn't work for this use-case. ~~Hunting for~~ Found the answer. :)

Some quick commands:

  The really cool streaming Heroku log

  ```
  heroku logs --tail 

  ```
  Run any scraper manually; Can also be used to initialize Heroku Schedulers

  ```
  heroku run scrapy crawl [crawler_name] -a city=? -a url=? -a sec=? -s AppId='INSERT ID HERE' -s ApiKey='INSERT KEY HERE'

  Note: If not on Heroku, drop heroku run.
  ```

You will need to have a place to store whatever you scrape.
I used Parse.com for this project and it's working great. 
The main issue with Parse is that they bill by API request. 

In the pipelines I'm sending a JSON blob to Parse when a scrape completes and 
processing the data while I save it and set it for a job to pickup later that 
sends out an email if one has never been sent before. If it has, it's skipped. 


The following is NOT EFFICIENT, but it will give you an idea 
of where you need to start. The code below was used during development to get 
this working. If you want to use this code, change the pipelines.py file. Use 
what is commented out and comment out the current code. This will make the code 
below work, but look at your API requets after a day. Mine hit 400K. YIKES :(

I'm sailing under 10K a day running 24/7 now!!! Figure out how yourself... lol


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
