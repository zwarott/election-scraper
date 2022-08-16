# Election Scraper
### Get electoral data for the Chamber of Deputies of the Parliament of the Czech Republic in 2017.

The purpose of this code is to create `csv` file that will contain electoral data for all municipalities (LAU2) in selected district (LAU1).

### # STEP 1: Libraries and modules
Required libraries and modules (see file "requirements.txt"):
- [*Requests*](https://requests.readthedocs.io/en/latest/) -> install via terminal -> `pip install requests`,
- [*Beautiful Soup*](https://beautiful-soup-4.readthedocs.io/en/latest/) -> install via terminal -> `pip install beautifulsoup4`,
- re -> installation is not required (built-in module),
- os -> installation is not required (built-in module),
- sys -> installation is not required (built-in module),
- csv -> installation is not required (built-in module).

### # STEP 2: Run the script `election_scraper.py`
To run the script it is necessary to write 3 arguments into the IDE terminal:
- **the first argument**: python argument in IDE terminal.
```
python
``` 

- **the second argument**: URL of selected district
  - click on [*here*](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) -> select certain district by clicking on 
  
  ![image](https://user-images.githubusercontent.com/107031859/184289201-4e0880bb-70f5-44a1-ab89-3d3bc7481135.png)

  - copy and paste URL into the second parameter in IDE terminal:
  ```
  "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6201"
  ```

- **the third argument**: define name of output file in format `csv`
  ```
  "lau1_blansko.csv"
  ```
Code in IDE terminal:
  ```
  python "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6201" "lau1_blansko.csv"
  ```
### # STEP 3: Output `csv` file

See `lau1_blansko.csv`

<img width="876" alt="output_overview" src="https://user-images.githubusercontent.com/107031859/184827452-39a7b368-001e-4f5e-9c13-075a3b5a4a75.png">

