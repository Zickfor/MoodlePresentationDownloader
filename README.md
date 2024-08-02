# MoodlePresentationDownloader

My small script for saving Moodle presentations in PDF.

# How to use?
1. Install requerments:
```
pip install selenium toml img2pdf
```
2. Start script.
3. Edit auto created **config.toml**
  * In section *auth* edit your Moodle username, password and url of Moodle itself
  * In *urls* put direct urls to necessary presentations).
  * Example:
```toml
urls = [ "https://example.com/mod/page/view.php?id=124118", "https://example.com/mod/page/view.php?id=124119", "https://example.com/mod/page/view.php?id=124120",]

[auth]
username = "admin"
password = "superstrongpassword"
moodle_url = "https://example.com/"

```
4. Start script again.
5. Watch the results!
6. On the next script executions just change urls list.
