module "s3" {
  source = "./s3"
}

module "glue" {
  source = "./glue"
}

module "kinesis" {
  source = "./kinesis"
}

module "iam" {
  source = "./iam"
}