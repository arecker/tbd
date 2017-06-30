# TBD

[![Build Status](https://travis-ci.org/arecker/tbd.svg?branch=master)](https://travis-ci.org/arecker/tbd) [![Coverage Status](https://coveralls.io/repos/arecker/tbd/badge.svg?branch=master&service=github)](https://coveralls.io/github/arecker/tbd?branch=master)

Write CloudFormation templates with jinja2.

```
{
  "Resources": {
    "Vpc": {
      "Type": "AWS::EC2::VPC",
      "Properties": {
	"CidrBlock": "10.0.0.0/16",
	"Tags": {{ tags(Name=ref('AWS::StackName')) | json }}
      }
    }
  }
}
```

Write your own custom macros.

```python
from tbd import register_function

@register_function
def my_vpc(cidr):
    return {
	"Type": "AWS::EC2::VPC",
	"Properties": {
	    "CidrBlock": cidr
	}
    }
```

```yaml
Resources:
  Vpc: {{ my_vpc('10.0.0.0/16') | yaml }}
```
