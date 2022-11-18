## AWS EC2 Auto Scaling Demo
Before we have to create our own ami.
```sh
cd packer-ali
packer build packer-template.json
```

Creating infascructure and deployment
> Do not forget to change local variables.
```sh
cd terraform
terraform init
terraform apply --auto-approve
```