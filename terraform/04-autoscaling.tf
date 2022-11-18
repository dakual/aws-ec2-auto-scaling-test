resource "aws_launch_template" "main" {
  name                   = "${local.name}-template"
  image_id               = local.ami
  key_name               = local.key_name
  vpc_security_group_ids = [ aws_security_group.main.id ]
}

resource "aws_autoscaling_group" "main" {
  name     = "${local.name}-ag"
  min_size = 1
  max_size = 3

  health_check_type   = "EC2"
  vpc_zone_identifier = aws_subnet.private.*.id
  target_group_arns   = [ aws_lb_target_group.main.arn ]

  mixed_instances_policy {
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.main.id
      }
      override {
        instance_type = "t2.micro"
      }
    }
  }
}

resource "aws_autoscaling_policy" "main" {
  name                   = "${local.name}-as-policy"
  policy_type            = "TargetTrackingScaling"
  autoscaling_group_name = aws_autoscaling_group.main.name

  estimated_instance_warmup = 300

  target_tracking_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ASGAverageCPUUtilization"
    }

    target_value = 50.0
  }
}