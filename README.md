
<!-- Find and Replace All [repo_name] -->
<!-- Replace [product-screenshot] [product-url] -->
<!-- Other Badgets https://naereen.github.io/badges/ -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
<!-- [![License][license-shield]][license-url] -->


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
	<!-- <li><a href="#license">License</a></li> -->
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project is a loan application that prompts the user to enter financial and private data to determine if an applicant qualifies for a loan and the type of loan the applicant qualifies for. It also asks the user to save the qualifying loans as a new CSV file

### Built With

<!-- This section should list any major frameworks that you built your project using. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples. -->

* [Python](https://www.python.org/)
* [Python CSV Reading/Writing](https://docs.python.org/3/library/csv.html)
* [Python fire](https://pypi.org/project/fire/)
* [Python questionary](https://pypi.org/project/questionary/)

<!-- GETTING STARTED -->
## Getting Started

<!-- This is an example of how you may give instructions on setting up your project locally. To get a local copy up and running follow these simple example steps. -->

### Prerequisites

<!-- This is an example of how to list things you need to use the software and how to install them. -->
* Python

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/AnaIitico/loan_qualifier_app.git
   ```
2. Install pip - package installer for Python
   [here](https://pip.pypa.io/en/stable/installation/)
3. Install Python packages
   ```sh
   pip install fire
   pip install questionary
   ```

<!-- USAGE EXAMPLES -->
## Usage

<!-- Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources. -->
This project is a loan application that prompts the user to enter financial and private data to determine if an applicant qualifies for a loan and the type of loan the applicant qualifies for. It also asks the user to save the qualifying loans as a new CSV file.

<!-- ROADMAP -->
## Roadmap

Here are some screenshots and code snippets of the working app

#### Confirm Dialogue - Enter No and exit the program
![Confirm Dialogue Screen Shot][confirm-screenshot]

#### Qualified Loans - saves to the qualified_loans folder
![Qualified Loan Screen Shot][qualifiedloan-screenshot]


#### Unqualified Loans - saves to the unqualified_loans folder
![Unqualified Loan Screen Shot][unqualifiedloan-screenshot]


#### Enter Name - forces a retry. User can then enter y/n
![Enter Name Screen Shot][entername-screenshot]


#### Save Function
  ```sh
  def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.
        Requires confirmation before saving the file
        Provides instructions for the file naming convention
        Includes logic to avoid empty filenames
        
    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    #Ask if the user wants to save the file
    question = questionary.confirm("Would you like to save the new file?").ask()

    if question == False:
        print("")
        print("Thank you for using the app. Goodbye!")
        quit()
    else:
        # Enter the new file name to be saved by the application
        name = questionary.text("""Enter the new file name by following these rules:
        1. Use lowercase letters
        2. Don't leave empty spaces between words.
        3. Use the underscore _ as a separator.
        4. Include .csv at the end of the name.
        5. For example: john_doe.csv"""
        ).ask()

        if name == "":
            print("")
            print("You must enter a file name")
            print("")
            save_qualifying_loans(qualifying_loans)
        
        if len(qualifying_loans) == 0:
            output_path = Path(f"results/unqualified_loans/{name.lower()}")
            save_csv(output_path, qualifying_loans)
        else:
            output_path = Path(f"results/qualified_loans/{name.lower()}")
            save_csv(output_path, qualifying_loans)
   ```

#### Save to CSV Function 
  ```sh
  def save_csv(output_path, qualifying_loans):
    """Saves the CSV file from path provided by user input.
        Checks to make sure the file was written and notifies the user

    Args:
        output_path (Path): The csv file output path from user input.
        qualifying_loans : List of qualifying loans from calculations.

    Saves:
        A list that contains the rows of qualifying loans for a customer.

    """
    header = ["Lender", "Max Loan Amount", "Max LTV", "Max DTI", "Min Credit Score", "Interest Rate"]
    with open(output_path, 'w', newline = '') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)

        for loans in qualifying_loans:
            csvwriter.writerow(loans)
        if os.path.isfile(output_path):
            print(f'The file {csvfile.name} was successfully written')
        else:
            print(f'The file {output_path} was not written')
  ```

See the [open issues](https://github.com/FalohT/Loan_Qualifier_App/issues) for a list of proposed features (and known issues).

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
<!-- ## License

Distributed under the MIT License. See `LICENSE` for more information.
 -->

<!-- CONTACT -->
## Contact

Oluwatobi Falolu - [@oluwatobi Falolu][linkedin-url] - falolu4@gmail.com

Project Link: [https://github.com/FalohT/Loan_Qualifier_App](https://github.com/FalohT/Loan_qualifier_app)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/AnaIitico/loan_qualifier_app.svg?style=for-the-badge
[contributors-url]: https://github.com/AnaIitico/loan_qualifier_app/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/AnaIitico/loan_qualifier_app.svg?style=for-the-badge
[forks-url]: https://github.com/AnaIitico/loan_qualifier_app/network/members
[stars-shield]: https://img.shields.io/github/stars/AnaIitico/loan_qualifier_app.svg?style=for-the-badge
[stars-url]: https://github.com/AnaIitico/loan_qualifier_app/stargazers
[issues-shield]: https://img.shields.io/github/issues/AnaIitico/loan_qualifier_app/network/members?style=for-the-badge
[issues-url]: https://github.com/AnaIitico/loan_qualifier_app/issues
<!-- [license-shield]: 
[license-url]:  -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/josetollinchi/
[confirm-screenshot]: /images/confirm.JPG
[qualifiedloan-screenshot]: /images/qualified_loan.JPG
[unqualifiedloan-screenshot]: /images/unqualified_loan.JPG
[entername-screenshot]: /images/enter_name.JPG
