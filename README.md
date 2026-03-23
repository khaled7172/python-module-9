*This project has been created as part of the 42 curriculum by khhammou*

## Description

tar -xvf archive_name.tar
-x extract: tells tar to extract files from the archive
-v Verbose: lists the files being extracted on the terminal
-f File: specifies that the next argument is the archive file name
To extract to a specific directory
tar -xvf archive_name.tar -C /path/to/destination
when you clone on 42 pc:
pip install pydantic to make sure the file runs well ex0
ex1
what is cls?
cls is a class reference like self for instances
when you use @model_validator(mode="after")
pydantic calls the method on the class, not on an instance yet
its not needed here, but  method signature must incldue it
print(cls) #  <class '__main__.AlienContact'>


Cosmic Data is a space-themed data validation project built with Pydantic v2. It covers basic model creation, custom validation rules, and nested model relationships through three progressive exercises.

## Structure

- **ex0** - Space Station Data: Basic Pydantic `BaseModel` with `Field` validation
- **ex1** - Alien Contact Logs: Custom validation using `@model_validator` and `Enum` types
- **ex2** - Space Crew Management: Nested Pydantic models and complex mission validation rules

## Usage

```bash
python3 ex0/space_station.py
python3 ex1/alien_contact.py
python3 ex2/space_crew.py
```

## Requirements

- Python 3.10 or later
- Pydantic 2.x

Install dependencies:

```bash
pip install pydantic
```

### Instructions

You run this code by doing python3 file_name.py

## Resources

The internet

## AI Usage

Testing my code with test cases and helping me find syntax errors# python-module-9
