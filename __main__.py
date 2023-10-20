import pulumi
import pulumi_alicloud as alicloud


az = 'ap-southeast-5a'
#define current resources group
resource_group = alicloud.resourcemanager.ResourceGroup('env-sandbox',
    resource_group_name='env-sandbox',
    display_name="env-sandbox")

#create vpc with specific cidr block
vpc = alicloud.vpc.Network("vpcsandbox",
              cidr_block="10.0.0.0/12",
              resource_group_id=resource_group.id)

#create new vswitch with specific az and cidr block
vswitch = alicloud.vpc.Switch("vswitch-sandbox",
                      vpc_id=vpc.id,
                      cidr_block="10.11.0.0/24", 
                      zone_id=az)

#create specific security group
security_group = alicloud.ecs.SecurityGroup("sg-sandbox", 
                                   vpc_id=vpc.id,
                                   resource_group_id=resource_group.id)

#create specific security group rule for allow intranet ssh access
security_group_rule = alicloud.ecs.SecurityGroupRule("sg-sandbox-ssh-rule",
    type="ingress",
    ip_protocol="tcp",
    nic_type="intranet",
    policy="accept",
    port_range="22/22",
    priority=1,
    security_group_id=security_group.id,
    cidr_ip="0.0.0.0/0"
)

#create new ecs instance
ecs_instance = alicloud.ecs.Instance("ecs-sandbox",
    instance_type="ecs.t5-lc1m1.small",
    security_groups=[security_group.id],
    availability_zone=az,
    vswitch_id=vswitch.id,
    image_id="centos_7_8_x64_20G_alibase_20211130.vhd",
    instance_name="ecs-sandbox",
    internet_charge_type="PayByTraffic",
    system_disk_category="cloud_efficiency",
    resource_group_id=resource_group.id
)

#output execution of each alibaba cloud information
pulumi.export("vpcId", vpc.id)
pulumi.export("vswitchId", vswitch.id)
pulumi.export("securityGroupId", security_group.id)
pulumi.export("ecsInstanceId", ecs_instance.id)
pulumi.export("resourceGroupId", resource_group.id)
