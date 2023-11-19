# **Phishing Website Detection using Machine Learning**

### Machine Learning Algorithms Used:

* Logistic Regression
* Support Vector Machine
* MLP Classifier
* Random Forest
* Decision Tree

### Training and Testing Accuracy for each model

![](/assets/accuracy.png)

### Feature Extraction Dictionary
```python
features = {
        'url_length': len(url),  # Length of URL
        'domain_length': len(domain),  # Length of domain
        'dot_count': domain.count('.'),  # Number of dots in the domain
        'is_ip_address': domain.replace('.', '').isdigit(),  # IP address in the domain
        'special_chars_in_domain': any(char.isnumeric() or not char.isalnum() for char in domain),  # Presence of special characters in the domain
        'tld_length': len(suffix),  # Length of the top-level domain (e.g., '.com', '.org')
        'hyphen_in_domain': '-' in domain,  # Presence of hyphen in the domain
        'at_symbol': '@' in parsed_url.netloc  # Presence of '@' in the URL
    }
```

