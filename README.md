<img src="docs/images//ESCAP_LOGO_OFFICIAL.png" alt="drawing" width="200"/>

# ESCAP training on Reproducible Analytic Pipelines for Consumer Price Statistics

This repo stores all content on the training done by UN ESCAP on Reproducible Analytic Pipelines (RAP) during September 2024, specifically for the consumer price statistics use case of web scraping a retailer website. 2 classes are given: a virtual one to introduce the topic and an in-person one to go into more detail.

# Training content

Check out the training content on the main site: https://sergegoussev.github.io/ESCAP_RAP_class/docs/

# Folder structure

```
├── notebooks               # Exploration notebooks for research purposes such as demo scraper notebook
├── demo_scraper            # Demo reproducible analytic pipeline that scrapes a site
├── data                    # Placeholder folders for the scraped data part of the demo, structure set up but it will be kept local
│   ├── raw                 # For raw scraped data before its cleaned for downstream use
│   └── final               # Cleaned data for downstream use
├── docs                    # Folder for documentation site that accompanies the demo scraper and also the class. Rendered via quarto
│   ├── images              # Images and diagrams for the documentation
│   └── teaching_material   # The actual materials for the 2 sessions
│       ├── sept_11         # Slides and latex material for the September 11th virtual session
│       └── sept_18         # Slides and latex material for the September 18th in person session
└── tests                   # Tests for the package
```

