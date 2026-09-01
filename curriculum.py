"""
Content data for the AWS SAA-C03 16-week prep app.
Each week: num, title, domain, intro, topics (name, explanation),
hands_on (list of task strings), quiz (list of question dicts).
"""

WEEKS = [
    {
        "num": 1,
        "title": "Foundations",
        "domain": "Foundations",
        "intro": "Before any service-specific detail, you need the vocabulary AWS uses everywhere else. This week is short on purpose.",
        "topics": [
            ("Regions & Availability Zones",
             "A Region is a physical location in the world (like us-east-1 in Virginia). Each Region contains "
             "multiple Availability Zones (AZs) — think of an AZ as one or more separate data centers with their "
             "own power, cooling, and networking. If one AZ has a problem, the others keep running. When you "
             "design something 'highly available,' you almost always mean 'spread across at least 2 AZs.'"),
            ("Edge locations",
             "Smaller AWS sites, in far more cities than Regions, used by CloudFront (AWS's CDN) to cache content "
             "close to users so it loads faster."),
            ("The Well-Architected Framework",
             "A checklist AWS created with 6 'pillars' you can hold any design up against: Operational Excellence, "
             "Security, Reliability, Performance Efficiency, Cost Optimization, and Sustainability. You won't "
             "recite the pillars often, but every scenario question is secretly testing one of them."),
            ("Shared Responsibility Model",
             "AWS is responsible for security 'of the cloud' — physical data centers, hardware, the network "
             "backbone. You are responsible for security 'in the cloud' — your data, your IAM permissions, your "
             "OS patches (for EC2), your network configuration. The more 'managed' a service is (Lambda vs EC2), "
             "the more AWS takes off your plate."),
        ],
        "hands_on": [
            "Open a free tier AWS account (if you don't already have one).",
            "Turn on MFA on the root user.",
            "Set a CloudWatch billing alarm for $5.",
        ],
        "quiz": [
            {"q": "A company wants its application to keep running even if an entire AWS data center loses power. What should they do?",
             "options": ["Deploy to multiple Availability Zones within a Region", "Deploy to multiple Regions only", "Use a single large EC2 instance", "Enable CloudFront"],
             "answer": 0,
             "explanation": "An AZ failure is a data-center-level failure. Spreading across AZs within one Region is the standard, lowest-cost way to survive that. Multi-Region is for disasters that take out an entire geographic area, not the default answer."},
            {"q": "Which of these is AWS's responsibility under the Shared Responsibility Model, even when you're running EC2 instances?",
             "options": ["Patching the operating system", "Configuring security groups", "Physical security of the data center", "Managing IAM policies"],
             "answer": 2,
             "explanation": "For EC2 (an unmanaged/IaaS service), you own the OS, network config, and IAM. AWS always owns the physical facility, hardware, and global network, regardless of which service you use."},
            {"q": "What is the main purpose of an AWS edge location?",
             "options": ["Running EC2 instances", "Caching content closer to end users for lower latency", "Storing IAM policies", "Hosting an entire Region's compute capacity"],
             "answer": 1,
             "explanation": "Edge locations exist in far more cities than full Regions and are used by CloudFront to serve cached content quickly."},
            {"q": "You want a low-cost way to avoid a surprise AWS bill while you're learning. What should you set up first?",
             "options": ["A CloudWatch billing alarm", "A second AWS account", "A Reserved Instance", "An Auto Scaling group"],
             "answer": 0,
             "explanation": "A billing alarm notifies you once costs cross a threshold you choose — cheap insurance while experimenting."},
            {"q": "Which Well-Architected pillar is a design decision to use Spot Instances primarily addressing?",
             "options": ["Security", "Reliability", "Cost Optimization", "Operational Excellence"],
             "answer": 2,
             "explanation": "Spot Instances trade availability guarantees for a much lower price — a cost-optimization tradeoff."},
            {"q": "A single Region typically contains:",
             "options": ["Exactly one Availability Zone", "Multiple isolated Availability Zones", "Multiple other Regions", "No edge locations"],
             "answer": 1,
             "explanation": "Regions are made of multiple AZs (usually 3+) specifically so workloads can be spread out for resilience."},
        ],
    },
    {
        "num": 2,
        "title": "IAM, part 1",
        "domain": "Security",
        "intro": "IAM controls who can do what. It's the single most-tested topic on the exam, so we start here and spend two weeks on it.",
        "topics": [
            ("Users, groups, policies, roles",
             "A User is one identity (a person or app) with long-term credentials. A Group bundles users together "
             "so you can attach one policy to all of them at once. A Policy is a JSON document that says what's "
             "allowed or denied. A Role is like a temporary user with no permanent credentials — anyone (or "
             "anything) can 'assume' it and get temporary permissions. Best practice: humans get Users in groups; "
             "AWS services (EC2, Lambda) get Roles, never long-term keys."),
            ("Identity-based vs resource-based policies",
             "An identity-based policy is attached to a user/group/role and says 'this identity can do X.' A "
             "resource-based policy is attached to a resource (like an S3 bucket) and says 'these identities can "
             "do X to me.' Resource-based policies are the only way to grant access to a different AWS account "
             "without a role."),
            ("How a policy is evaluated",
             "AWS checks all applicable policies. If any policy has an explicit Deny, that wins immediately, no "
             "matter what else says Allow. If there's no explicit Deny, AWS looks for at least one Allow. If it "
             "finds none, the default is Deny. Memorize: explicit Deny > explicit Allow > default Deny."),
        ],
        "hands_on": [
            "Create an IAM user with a custom, limited-access policy (e.g., read-only S3).",
            "Create a role for EC2 and attach an S3 access policy to it.",
            "Confirm the EC2 instance can reach S3 with no access keys stored anywhere.",
        ],
        "quiz": [
            {"q": "An application running on EC2 needs to read from an S3 bucket. What's the best-practice way to grant this?",
             "options": ["Store an IAM user's access keys in the EC2 instance", "Attach an IAM role to the EC2 instance", "Make the S3 bucket public", "Hard-code the keys in the application"],
             "answer": 1,
             "explanation": "Roles provide temporary, automatically-rotated credentials with no keys to leak — always preferred over storing access keys on an instance."},
            {"q": "A policy attached to a user allows S3 access. A separate policy explicitly denies deleting objects. What happens when the user tries to delete an object?",
             "options": ["It succeeds because Allow was found first", "It's denied because explicit Deny always wins", "AWS asks the user to choose", "It succeeds because there are more Allow statements"],
             "answer": 1,
             "explanation": "Explicit Deny always overrides any Allow, regardless of how many Allow statements exist."},
            {"q": "You need to grant a partner's separate AWS account read access to one of your S3 buckets, without creating an IAM user for them. What should you use?",
             "options": ["An identity-based policy on your own users", "A resource-based bucket policy", "A security group", "A NACL"],
             "answer": 1,
             "explanation": "Resource-based policies (like S3 bucket policies) can grant access to principals in other AWS accounts directly, no role assumption or user creation required."},
            {"q": "By default, if no policy explicitly allows or denies an action, what happens?",
             "options": ["It's allowed", "It's denied", "It depends on the region", "AWS logs a warning but allows it"],
             "answer": 1,
             "explanation": "IAM's default is implicit deny — access must be explicitly granted."},
            {"q": "What's the difference between an IAM Role and an IAM User?",
             "options": ["Roles have permanent access keys, Users don't", "Roles provide temporary credentials that can be assumed; Users have long-term credentials", "There is no difference", "Roles can only be used by the root account"],
             "answer": 1,
             "explanation": "Roles are assumed temporarily (by users, services, or other accounts) and issue short-lived credentials via STS."},
            {"q": "You want ten new employees to all have the same S3 read access. What's the most efficient way?",
             "options": ["Copy the same policy onto 10 individual users", "Put them in a group and attach the policy once to the group", "Create 10 roles", "Create one shared IAM user for all of them"],
             "answer": 1,
             "explanation": "Groups let you manage permissions for many users in one place instead of repeating policies per user."},
        ],
    },
    {
        "num": 3,
        "title": "IAM, part 2",
        "domain": "Security",
        "intro": "The advanced half of IAM — controlling access across accounts and setting hard ceilings on permissions.",
        "topics": [
            ("Cross-account roles",
             "Lets a user or service in Account A assume a role in Account B to get temporary access, without "
             "needing a separate user in Account B. This is the standard way to let one account access resources "
             "in another."),
            ("Permission boundaries",
             "A permission boundary is a policy that sets the maximum permissions an identity can ever have, even "
             "if their other policies grant more. Used to let junior admins create users/roles without those "
             "users ever exceeding a safe limit."),
            ("AWS Organizations and SCPs",
             "Organizations let you manage many AWS accounts centrally. Service Control Policies (SCPs) set the "
             "maximum allowed actions for entire accounts or OUs (organizational units) — even the account's root "
             "user can't exceed an SCP's limits. SCPs don't grant permissions by themselves; they only restrict."),
            ("Explicit Deny vs no permission",
             "'No permission' (implicit deny) just means nothing granted it. 'Explicit Deny' is a policy statement "
             "that actively blocks it, and always wins over any Allow."),
        ],
        "hands_on": [
            "Build a cross-account role in a second (or sandbox) account.",
            "Practice assuming it via the CLI or the console's 'Switch Role.'",
        ],
        "quiz": [
            {"q": "A parent company wants to guarantee that no account in its Marketing OU can ever use EC2, regardless of what IAM policies exist in those accounts. What should they use?",
             "options": ["An IAM permission boundary", "A Service Control Policy on the OU", "A resource-based policy", "An identity-based policy"],
             "answer": 1,
             "explanation": "SCPs apply organization-wide caps on what accounts/OUs can do, overriding even account-level Allow policies."},
            {"q": "What does a permission boundary actually do?",
             "options": ["Grants permissions directly", "Sets the maximum permissions an identity can have, even with other allow policies", "Denies specific IP ranges", "Replaces IAM policies entirely"],
             "answer": 1,
             "explanation": "A boundary is a ceiling, not a grant — the identity still needs actual Allow policies within that ceiling."},
            {"q": "Which statement about SCPs is true?",
             "options": ["SCPs can grant new permissions", "SCPs can only restrict, never grant, permissions", "SCPs apply only to IAM users, not roles", "SCPs override MFA requirements"],
             "answer": 1,
             "explanation": "SCPs are filters on the maximum available permissions — they never add anything by themselves."},
            {"q": "A vendor's AWS account needs temporary access to a specific S3 bucket in your account. What's the standard secure pattern?",
             "options": ["Share your root credentials", "Create a cross-account IAM role they can assume", "Make the bucket public", "Give them a permanent IAM user in your account"],
             "answer": 1,
             "explanation": "Cross-account roles grant temporary, scoped, revocable access without sharing long-term credentials."},
            {"q": "If a resource has no policy statement addressing an action at all (no allow, no deny), what is the result?",
             "options": ["Allowed by default", "Denied by default", "It depends on which service", "The root user decides"],
             "answer": 1,
             "explanation": "IAM defaults to implicit deny in the absence of an explicit Allow."},
        ],
    },
    {
        "num": 4,
        "title": "Encryption and secrets",
        "domain": "Security",
        "intro": "Protecting data at rest and in transit, and keeping secrets out of your code.",
        "topics": [
            ("KMS keys: AWS-managed vs customer-managed",
             "KMS (Key Management Service) creates and controls encryption keys. AWS-managed keys are created and "
             "rotated automatically by AWS, with no control over policy. Customer-managed keys are keys you "
             "create, where you control the key policy, rotation, and who can use them — needed for fine-grained "
             "control or when you must disable/delete a key."),
            ("Encryption at rest and in transit",
             "'At rest' means data is encrypted while stored on disk (EBS, S3, RDS). 'In transit' means data is "
             "encrypted while moving over the network (TLS/HTTPS). Know which AWS feature covers each, per service."),
            ("Secrets Manager vs Parameter Store",
             "Both store secrets (passwords, API keys). Secrets Manager can automatically rotate credentials (e.g., "
             "RDS passwords) and costs more. Parameter Store (part of Systems Manager) is cheaper/free for the "
             "standard tier but has no built-in automatic rotation — better for config values and simple secrets."),
            ("ACM",
             "AWS Certificate Manager issues and renews free public TLS certificates for use with services like "
             "CloudFront, ALB, and API Gateway."),
        ],
        "hands_on": [
            "Create a customer-managed KMS key.",
            "Encrypt an S3 bucket with it.",
            "Create and encrypt an EBS volume with it too.",
        ],
        "quiz": [
            {"q": "A company needs an RDS database password to rotate automatically every 30 days without app downtime. What should they use?",
             "options": ["Parameter Store", "Secrets Manager", "KMS", "ACM"],
             "answer": 1,
             "explanation": "Secrets Manager has built-in automatic rotation for supported databases; Parameter Store does not do this natively."},
            {"q": "Which KMS key type gives you full control over the key policy and lets you disable or schedule deletion of the key?",
             "options": ["AWS-managed key", "Customer-managed key", "AWS-owned key", "Default S3 key"],
             "answer": 1,
             "explanation": "Customer-managed keys are the only KMS key type where you control the key policy and lifecycle."},
            {"q": "What does 'encryption in transit' protect against?",
             "options": ["Someone reading data off a stolen hard drive", "Someone intercepting data as it travels over the network", "Someone guessing an IAM password", "Malware on the client machine"],
             "answer": 1,
             "explanation": "In-transit encryption (TLS) protects data while it moves between systems, not while it's sitting on storage."},
            {"q": "Where would you go to get a free public TLS/SSL certificate for a CloudFront distribution?",
             "options": ["KMS", "ACM", "Secrets Manager", "IAM"],
             "answer": 1,
             "explanation": "ACM issues and auto-renews public certificates for integration with CloudFront, ALB, API Gateway, etc."},
            {"q": "A startup wants to store a simple config value (not a rotating secret) as cheaply as possible. What's the best fit?",
             "options": ["Secrets Manager", "Systems Manager Parameter Store", "KMS", "IAM policy"],
             "answer": 1,
             "explanation": "Parameter Store's standard tier is free and fits plain configuration values well; Secrets Manager is built for secrets that need rotation and costs more per secret."},
        ],
    },
    {
        "num": 5,
        "title": "VPC, part 1",
        "domain": "Security",
        "intro": "Networking is where the exam gets visual. Build the VPC by hand this week so it clicks.",
        "topics": [
            ("Subnets",
             "A subnet is a slice of your VPC's IP range tied to one Availability Zone. A subnet is 'public' if "
             "its route table sends 0.0.0.0/0 traffic to an Internet Gateway; otherwise it's 'private.'"),
            ("Route tables",
             "A route table is the map of 'where does traffic for this destination go.' Every subnet uses exactly "
             "one route table, though many subnets can share the same one."),
            ("Internet gateway",
             "Attached to the VPC, it's what allows resources in public subnets to reach the internet (and be "
             "reached from it, if they have a public IP)."),
            ("NAT gateway",
             "Lives in a public subnet and lets resources in private subnets initiate outbound internet "
             "connections (e.g., to download updates) without being reachable from the internet."),
            ("CIDR blocks",
             "The notation (like 10.0.0.0/16) that defines a range of IP addresses. A smaller number after the "
             "slash means more addresses — a /16 has far more IPs than a /24."),
        ],
        "hands_on": [
            "Build a VPC by hand (no wizard): 2 public subnets and 2 private subnets, across 2 AZs.",
            "Add route tables, an Internet Gateway, and a NAT Gateway.",
        ],
        "quiz": [
            {"q": "What makes a subnet 'public'?",
             "options": ["It has a large CIDR block", "Its route table has a route to an Internet Gateway", "It contains an RDS instance", "It has no NACL"],
             "answer": 1,
             "explanation": "A subnet is public specifically because its route table sends internet-bound traffic to an IGW — nothing else defines 'public.'"},
            {"q": "An EC2 instance in a private subnet needs to download OS updates from the internet, but should never be reachable from the internet. What do you add?",
             "options": ["An Internet Gateway directly to the private subnet", "A NAT Gateway in a public subnet", "A VPC peering connection", "A wider CIDR block"],
             "answer": 1,
             "explanation": "NAT Gateway allows outbound-only internet access for private subnets, exactly this pattern."},
            {"q": "What does the CIDR block 10.0.0.0/24 provide compared to 10.0.0.0/16?",
             "options": ["The same number of IPs", "Far fewer IPs (a /24 is much smaller)", "Far more IPs", "No IPs, it's invalid"],
             "answer": 1,
             "explanation": "A smaller CIDR prefix number (like /16) covers more addresses; a larger prefix number (like /24) covers fewer."},
            {"q": "How many Availability Zones should a highly-available VPC design span, at minimum?",
             "options": ["1", "2", "5", "All AZs in every Region"],
             "answer": 1,
             "explanation": "Spreading across at least 2 AZs is the standard minimum for resilience without over-provisioning."},
            {"q": "What component is required for resources in a public subnet to be reachable from the internet?",
             "options": ["NAT Gateway", "An Internet Gateway attached to the VPC, plus a route to it", "VPC peering", "A private CIDR block"],
             "answer": 1,
             "explanation": "The Internet Gateway is the door between the VPC and the internet; the route table must point to it for a subnet to be 'public.'"},
        ],
    },
    {
        "num": 6,
        "title": "VPC, part 2",
        "domain": "Security",
        "intro": "Firewalls inside the VPC, private paths to AWS services, and connecting networks together.",
        "topics": [
            ("Security groups vs NACLs",
             "Security groups are stateful and attached to instances/ENIs — allow inbound traffic and the response "
             "is automatically allowed out, and SGs can only Allow (never explicitly Deny). NACLs are stateless "
             "and attached to subnets — you must explicitly allow both inbound and outbound, and NACLs can "
             "explicitly Deny. Rule of thumb: SG = instance-level allow-list, NACL = subnet-level firewall with "
             "allow and deny."),
            ("VPC endpoints: gateway vs interface",
             "A VPC endpoint lets resources in your VPC reach an AWS service without going over the public "
             "internet. Gateway endpoints (S3, DynamoDB only) are free and work via route table entries. Interface "
             "endpoints (most other services) create an ENI with a private IP in your subnet and cost a small "
             "hourly fee."),
            ("Peering, Transit Gateway, Site-to-Site VPN, Direct Connect",
             "Peering connects two VPCs directly (1:1, no transitive routing). Transit Gateway is a hub that "
             "connects many VPCs and on-prem networks together, avoiding the 'full mesh' problem of many peering "
             "connections. Site-to-Site VPN is an encrypted connection over the public internet to your on-prem "
             "network. Direct Connect is a dedicated private physical network link to AWS — faster and more "
             "consistent, but takes weeks to provision."),
        ],
        "hands_on": [
            "Add an S3 gateway endpoint to a VPC.",
            "Confirm a private EC2 instance can reach S3 with zero internet access (no NAT, no IGW).",
        ],
        "quiz": [
            {"q": "You need dozens of VPCs and on-premises networks to all reach each other without a tangle of point-to-point connections. What should you use?",
             "options": ["VPC Peering for every pair", "Transit Gateway", "NAT Gateway", "Security Groups"],
             "answer": 1,
             "explanation": "Transit Gateway acts as a central hub, avoiding the full-mesh scaling problem of pairwise VPC peering."},
            {"q": "Which statement about Security Groups is true?",
             "options": ["They are stateless and require explicit outbound rules for responses", "They are stateful, so return traffic is automatically allowed", "They can explicitly deny traffic", "They attach to subnets, not instances"],
             "answer": 1,
             "explanation": "Security groups are stateful (return traffic auto-allowed) and instance-level, and they can only allow, never explicitly deny."},
            {"q": "A private EC2 instance needs to reach S3 without using a NAT Gateway or any internet access. What should you add?",
             "options": ["An Interface endpoint", "A Gateway endpoint for S3", "A Site-to-Site VPN", "An Internet Gateway"],
             "answer": 1,
             "explanation": "S3 and DynamoDB support free Gateway endpoints, added via route table entries, keeping traffic off the public internet entirely."},
            {"q": "Your company needs a fast, dedicated, private physical network connection between its data center and AWS. What's the best fit?",
             "options": ["Site-to-Site VPN", "Direct Connect", "VPC Peering", "Transit Gateway"],
             "answer": 1,
             "explanation": "Direct Connect provides a dedicated physical link with more consistent performance than a VPN over the public internet, though it takes longer to provision."},
            {"q": "What's a key difference between a Network ACL and a Security Group?",
             "options": ["NACLs are stateful, Security Groups are stateless", "NACLs can explicitly deny traffic and operate at the subnet level; Security Groups cannot deny and operate at the instance level", "They are functionally identical", "Security Groups apply to subnets only"],
             "answer": 1,
             "explanation": "NACLs are stateless, subnet-level, and can explicitly deny. Security Groups are stateful, instance-level, and allow-only."},
        ],
    },
    {
        "num": 7,
        "title": "EC2 and storage",
        "domain": "Security",
        "intro": "The compute and storage building blocks that show up inside almost every other scenario question.",
        "topics": [
            ("Instance types and purchase options",
             "Instance types are named by family + size (e.g., m5.large) — the letter signals the purpose (t = "
             "burstable/general, c = compute, r = memory, i = storage). Purchase options: On-Demand (pay per "
             "second/hour, no commitment), Reserved (1-3 year commitment for a discount), Savings Plans (commit to "
             "a $/hour spend for a discount, more flexible than RIs), Spot (bid on spare capacity for up to ~90% "
             "off, can be reclaimed with a 2-minute warning), Dedicated Hosts (a physical server just for you, for "
             "compliance/licensing needs)."),
            ("AMIs and user data",
             "An AMI (Amazon Machine Image) is the template (OS + software) an EC2 instance launches from. User "
             "data is a script that runs automatically the first time an instance boots — used to install "
             "software or configure the instance at launch."),
            ("EBS volume types, snapshots, instance store, EFS",
             "EBS is network-attached block storage for one EC2 instance at a time, in types like gp3 (general "
             "purpose SSD), io2 (high-performance SSD), and st1/sc1 (cheap HDD for throughput/archival). Snapshots "
             "are point-in-time backups of an EBS volume, incremental after the first one. Instance store is "
             "physically attached, very fast, but ephemeral — data is lost if the instance stops. EFS is a "
             "managed, shared file system that many EC2 instances (across AZs) can mount at once, unlike EBS."),
        ],
        "hands_on": [
            "Launch an EC2 instance in a private subnet.",
            "Connect to it using Session Manager (no SSH key, no open port 22).",
        ],
        "quiz": [
            {"q": "A team needs a shared file system that hundreds of EC2 instances across multiple AZs can read and write simultaneously. What should they use?",
             "options": ["EBS", "EFS", "Instance store", "A single gp3 volume attached to all instances"],
             "answer": 1,
             "explanation": "EBS attaches to one instance at a time; EFS is the managed, multi-attach, multi-AZ shared file system."},
            {"q": "Which EC2 purchase option offers the deepest discount but can be reclaimed by AWS with only a 2-minute warning?",
             "options": ["Reserved Instances", "On-Demand", "Spot Instances", "Dedicated Hosts"],
             "answer": 2,
             "explanation": "Spot Instances use spare capacity at steep discounts, but AWS can reclaim them on short notice — best for fault-tolerant/interruptible workloads."},
            {"q": "What happens to data on instance store storage if the underlying EC2 instance is stopped?",
             "options": ["It persists in S3 automatically", "It is lost", "It's automatically snapshotted", "It moves to EFS"],
             "answer": 1,
             "explanation": "Instance store is physically attached ephemeral storage — data does not survive a stop (though it survives a reboot)."},
            {"q": "What is the best-practice way to connect to an EC2 instance in a private subnet with no open inbound ports?",
             "options": ["SSH with a key pair over the internet", "AWS Systems Manager Session Manager", "Open port 22 to 0.0.0.0/0", "A bastion host with a public IP always"],
             "answer": 1,
             "explanation": "Session Manager uses the SSM agent and IAM permissions — no open inbound ports, no SSH keys, and full audit logging."},
            {"q": "What is a user data script used for?",
             "options": ["Storing IAM credentials", "Running configuration/setup commands automatically the first time an instance boots", "Creating an AMI", "Attaching an EBS volume"],
             "answer": 1,
             "explanation": "User data runs once at first boot, commonly to install packages or configure the instance without manual work."},
        ],
    },
    {
        "num": 8,
        "title": "S3 + first checkpoint",
        "domain": "Security",
        "intro": "The last new security-domain topic, then your first real progress checkpoint: a build and a full practice exam.",
        "topics": [
            ("Storage classes",
             "S3 Standard (frequent access), Standard-IA / One Zone-IA (infrequent access, cheaper storage but a "
             "retrieval fee, One Zone = single AZ, cheaper but less durable), Glacier family (archival, retrieval "
             "takes minutes to hours, cheapest storage), Intelligent-Tiering (automatically moves objects between "
             "tiers based on access patterns — good when access patterns are unpredictable)."),
            ("Lifecycle rules",
             "Automated rules that transition objects between storage classes or expire (delete) them after a set "
             "number of days — e.g., 'move to Glacier after 90 days, delete after 365.'"),
            ("Versioning",
             "Keeps every version of an object when enabled, so an overwrite or delete doesn't destroy the "
             "previous version — protects against accidental deletion/overwrite."),
            ("Bucket policies",
             "Resource-based policies attached directly to a bucket, controlling who (which principals, even other "
             "accounts) can do what to it."),
            ("Replication",
             "Automatically copies objects to another bucket, either in the same Region (SRR) or a different "
             "Region (CRR) — used for compliance, latency, or disaster recovery."),
            ("Presigned URLs",
             "A temporary URL that grants time-limited access to a specific private object, without making the "
             "object or bucket public."),
        ],
        "hands_on": [
            "Project 1: build a two-tier web app — web server in a public subnet, database in a private subnet, static files in S3.",
            "Take your first full practice exam. Expect a low score — that is normal and it is information, not failure.",
        ],
        "quiz": [
            {"q": "A company needs objects available immediately, but access patterns are unpredictable and they don't want to manually manage tiers. What storage class fits best?",
             "options": ["S3 Standard-IA", "S3 Glacier", "S3 Intelligent-Tiering", "S3 One Zone-IA"],
             "answer": 2,
             "explanation": "Intelligent-Tiering automatically moves objects between access tiers based on actual usage, ideal for unpredictable patterns."},
            {"q": "How do you give a user temporary access to download one private S3 object, without making it public?",
             "options": ["A bucket policy allowing '*'", "A presigned URL", "Enable public read on the object", "Turn on versioning"],
             "answer": 1,
             "explanation": "Presigned URLs grant time-limited access to one object using the permissions of the URL's creator, without changing the object's or bucket's public access settings."},
            {"q": "What protects an S3 object from being permanently lost if someone accidentally overwrites it?",
             "options": ["Lifecycle rules", "Versioning", "Cross-Region Replication alone", "Intelligent-Tiering"],
             "answer": 1,
             "explanation": "With versioning on, an overwrite creates a new version rather than destroying the old one, so you can restore it."},
            {"q": "A compliance requirement says backups of certain S3 objects must exist in a different AWS Region. What feature addresses this directly?",
             "options": ["Lifecycle rules", "Cross-Region Replication", "Presigned URLs", "One Zone-IA"],
             "answer": 1,
             "explanation": "CRR automatically copies objects to a bucket in another Region, satisfying geographic redundancy/compliance needs."},
            {"q": "You scored 45% on your first full practice exam at week 8. What should you conclude?",
             "options": ["You should quit and try a different certification", "This is a normal, expected checkpoint score at this stage", "The practice exam is broken", "You need to memorize more services"],
             "answer": 1,
             "explanation": "The plan explicitly calls out a low first practice score as expected information, not failure — it tells you where to focus for the rest of the plan."},
        ],
    },
    {
        "num": 9,
        "title": "Load balancing and scaling",
        "domain": "Resilience",
        "intro": "Part 2 of the plan begins: keeping applications up and responsive as load changes.",
        "topics": [
            ("ALB vs NLB vs Gateway LB",
             "ALB (Application Load Balancer) works at Layer 7 (HTTP/HTTPS), can route based on path/host, good "
             "for web apps. NLB (Network Load Balancer) works at Layer 4 (TCP/UDP), handles massive throughput "
             "with ultra-low latency, gives a static IP — good for non-HTTP or extreme performance needs. Gateway "
             "Load Balancer is used to insert third-party virtual appliances (firewalls, intrusion detection) "
             "transparently into the traffic path."),
            ("Target groups, health checks",
             "A target group is the set of instances (or IPs, or Lambda functions) a load balancer sends traffic "
             "to. Health checks periodically test each target; unhealthy targets stop receiving traffic until "
             "they pass again."),
            ("Auto Scaling groups and policies",
             "An ASG keeps a fleet of instances running, launching or terminating them to match demand. Scaling "
             "policies decide when: target tracking (keep a metric like CPU at X%), step scaling (react in "
             "increments to alarm thresholds), scheduled scaling (known traffic patterns, e.g. scale up every "
             "weekday morning)."),
            ("Multi-AZ design",
             "Putting instances of an ASG behind a load balancer, spread across multiple AZs, so no single AZ "
             "failure takes the app down."),
        ],
        "hands_on": [
            "Put your Project 1 web server behind an ALB with an Auto Scaling group.",
            "Kill an instance and watch it get replaced automatically.",
        ],
        "quiz": [
            {"q": "An application needs to route requests to different target groups based on URL path (e.g., /api vs /images). Which load balancer fits?",
             "options": ["NLB", "ALB", "Gateway Load Balancer", "Classic Load Balancer"],
             "answer": 1,
             "explanation": "ALB operates at Layer 7 and supports content-based routing like path- and host-based rules; NLB only works at the connection/packet level (Layer 4)."},
            {"q": "An app needs to handle millions of requests per second with ultra-low latency over raw TCP, and needs a static IP. Which load balancer fits?",
             "options": ["ALB", "NLB", "Gateway Load Balancer", "None, use Route 53 only"],
             "answer": 1,
             "explanation": "NLB is built for extreme performance and static IP support at Layer 4."},
            {"q": "What does an Auto Scaling Group's health check + target group combination achieve?",
             "options": ["It reduces cost automatically", "It stops sending traffic to instances that fail health checks and can replace them", "It encrypts traffic automatically", "It changes the instance type automatically"],
             "answer": 1,
             "explanation": "Health checks detect unhealthy targets; the ASG can terminate and replace them, and the load balancer stops routing to them until healthy."},
            {"q": "A retailer knows traffic spikes every day at 9am. What scaling policy fits best alongside target tracking?",
             "options": ["Manual scaling only", "Scheduled scaling", "Spot-only scaling", "No scaling, just oversize the fleet"],
             "answer": 1,
             "explanation": "Scheduled scaling proactively adds capacity ahead of a known, predictable pattern, rather than reacting after the fact."},
            {"q": "Why put ASG instances behind a load balancer spread across multiple AZs, instead of just one AZ?",
             "options": ["It's required by AWS billing", "So the app survives the loss of a single AZ", "It reduces IAM complexity", "It removes the need for security groups"],
             "answer": 1,
             "explanation": "Multi-AZ deployment behind a load balancer is the standard resilience pattern against single-AZ failures."},
        ],
    },
    {
        "num": 10,
        "title": "Databases",
        "domain": "Resilience",
        "intro": "Relational, caching, and NoSQL — and the Multi-AZ vs read replica distinction that shows up constantly.",
        "topics": [
            ("RDS",
             "A managed relational database service (MySQL, PostgreSQL, etc.) — AWS handles patching, backups, "
             "and failover setup for you."),
            ("Multi-AZ vs read replica",
             "Multi-AZ keeps a synchronous standby copy in another AZ purely for failover (disaster recovery) — "
             "you can't read from the standby, and it's the same Region. A read replica is an asynchronous copy "
             "used to offload read traffic (scaling reads), can be in the same or a different Region, and can be "
             "manually promoted to a standalone database if needed. Remember: Multi-AZ = availability, Read "
             "Replica = scalability — and they can be combined."),
            ("Aurora",
             "AWS's own MySQL/PostgreSQL-compatible database, more performant and more resilient than standard "
             "RDS. Storage automatically replicates across 3 AZs, and it supports up to 15 read replicas with "
             "much lower replication lag."),
            ("DynamoDB",
             "A managed NoSQL key-value/document database. The partition key determines which partition (physical "
             "storage segment) an item lives on — good partition key design avoids 'hot partitions.' On-demand "
             "mode auto-scales capacity and you pay per request; provisioned mode requires you to set read/write "
             "capacity ahead of time (cheaper if usage is predictable). DAX is an in-memory cache in front of "
             "DynamoDB for microsecond read latency. Global Tables replicate a DynamoDB table across multiple "
             "Regions with multi-active writes."),
            ("ElastiCache: Redis vs Memcached",
             "Both are managed in-memory caches that sit in front of a database to reduce load and latency. Redis "
             "supports persistence, replication, and complex data structures (use it by default). Memcached is "
             "simpler, multi-threaded, and used when you need pure, simple, easily-scalable caching with no "
             "persistence requirement."),
        ],
        "hands_on": [
            "Create an RDS instance with Multi-AZ enabled.",
            "Add a read replica to it.",
        ],
        "quiz": [
            {"q": "A company wants their production database to automatically fail over to a standby in a different AZ if the primary fails, with no manual intervention. What should they enable?",
             "options": ["A read replica", "RDS Multi-AZ", "DynamoDB Global Tables", "ElastiCache"],
             "answer": 1,
             "explanation": "Multi-AZ is specifically for automatic failover/availability, using a synchronous standby you can't read from directly."},
            {"q": "An app has heavy read traffic that's slowing down the primary database. What should they add to offload reads?",
             "options": ["Multi-AZ standby", "A read replica", "A bigger EBS volume", "Enable versioning"],
             "answer": 1,
             "explanation": "Read replicas are asynchronous copies specifically meant to scale out read traffic, unlike the Multi-AZ standby which cannot serve reads."},
            {"q": "Which database is AWS's own high-performance, MySQL/PostgreSQL-compatible engine with storage replicated across 3 AZs automatically?",
             "options": ["DynamoDB", "Aurora", "ElastiCache", "RDS SQL Server"],
             "answer": 1,
             "explanation": "Aurora is AWS's proprietary relational engine, built for higher performance/durability than standard RDS engines."},
            {"q": "A DynamoDB table is experiencing a 'hot partition' problem, with most traffic hitting one partition. What is most likely the cause?",
             "options": ["On-demand capacity mode", "A poorly chosen partition key", "Too many read replicas", "Missing DAX cache"],
             "answer": 1,
             "explanation": "The partition key determines how items are distributed; a low-cardinality or skewed key concentrates traffic on one partition."},
            {"q": "What does DAX add to a DynamoDB setup?",
             "options": ["Cross-Region replication", "A microsecond-latency in-memory read cache in front of DynamoDB", "Automatic schema migration", "SQL query support"],
             "answer": 1,
             "explanation": "DAX is DynamoDB's dedicated caching layer for very low read latency."},
            {"q": "You need an in-memory cache with built-in replication and persistence in front of your database. Redis or Memcached?",
             "options": ["Memcached", "Redis", "Either, they're identical", "Neither, use DAX"],
             "answer": 1,
             "explanation": "Redis supports persistence, replication, and richer data structures; Memcached is simpler with no persistence — choose based on those needs."},
        ],
    },
    {
        "num": 11,
        "title": "Decoupling and serverless",
        "domain": "Resilience",
        "intro": "Letting parts of a system fail or slow down independently, without taking the whole system down with them.",
        "topics": [
            ("SQS",
             "A managed message queue that decouples producers from consumers. Standard queues offer at-least-once "
             "delivery and best-effort ordering, at nearly unlimited throughput. FIFO queues guarantee "
             "exactly-once processing and strict ordering, but with lower throughput. Visibility timeout: once a "
             "consumer picks up a message, it's hidden from other consumers for a set time, so it isn't processed "
             "twice — if the consumer doesn't finish (delete it) in time, it reappears. A dead-letter queue is "
             "where messages go after failing processing too many times, so they don't loop forever and can be "
             "inspected later."),
            ("SNS",
             "A pub/sub notification service — one message published fans out to many subscribers at once (email, "
             "SQS queues, Lambda, SMS). Contrast with SQS: SNS pushes to many subscribers, SQS holds messages for "
             "one (or more competing) consumer(s) to pull."),
            ("EventBridge",
             "An event bus for routing events between AWS services and your own apps based on rules, with more "
             "filtering and third-party/SaaS integration than SNS."),
            ("Lambda",
             "Run code without managing servers — pay only for execution time, scales automatically, has a max "
             "execution time limit (15 minutes) so it's for short tasks, not long-running processes."),
            ("API Gateway",
             "Manages, secures, and exposes APIs (often in front of Lambda) — handles throttling, auth, and "
             "request/response transformation."),
            ("Step Functions",
             "Orchestrates multiple Lambda functions (or other services) into a visual workflow with retries, "
             "error handling, and branching logic."),
            ("ECS vs Fargate vs EKS",
             "ECS is AWS's own container orchestrator. Fargate is a serverless compute engine for containers — no "
             "EC2 servers to manage (works with both ECS and EKS). EKS is managed Kubernetes, for teams that "
             "specifically need Kubernetes compatibility/portability."),
        ],
        "hands_on": [
            "Build S3 upload -> Lambda -> SQS: an S3 event triggers a Lambda function, which puts a message onto an SQS queue.",
            "Watch the message arrive in the queue.",
        ],
        "quiz": [
            {"q": "An order needs to be processed exactly once, in the exact order it was placed. Which queue type fits?",
             "options": ["SQS Standard", "SQS FIFO", "SNS", "EventBridge"],
             "answer": 1,
             "explanation": "FIFO queues guarantee exactly-once processing and strict ordering; Standard queues trade that for higher throughput and only best-effort ordering."},
            {"q": "A message has failed processing repeatedly and keeps looping back into the queue. What SQS feature addresses this?",
             "options": ["Visibility timeout", "A dead-letter queue", "FIFO ordering", "Long polling"],
             "answer": 1,
             "explanation": "A DLQ catches messages after a max number of failed attempts, stopping the retry loop and letting you inspect them separately."},
            {"q": "You need one event (e.g., 'order placed') to trigger three different things at once: an email, a Lambda function, and an SQS queue. What's the best fit?",
             "options": ["SQS alone", "SNS", "A single Lambda function", "API Gateway"],
             "answer": 1,
             "explanation": "SNS is pub/sub — one publish fans out to many independent subscribers simultaneously, unlike SQS which is meant for one (or competing) consumers pulling from one queue."},
            {"q": "A workflow needs to run five Lambda functions in a specific order, with retry logic and branching based on results. What should orchestrate this?",
             "options": ["SNS", "Step Functions", "SQS", "CloudFront"],
             "answer": 1,
             "explanation": "Step Functions is built exactly for orchestrating multi-step workflows across services with built-in error handling and branching."},
            {"q": "A team wants to run containers without managing any EC2 instances at all. What should they use?",
             "options": ["EKS with self-managed nodes", "Fargate", "ECS with EC2 launch type", "An Auto Scaling Group of instances"],
             "answer": 1,
             "explanation": "Fargate is the serverless compute engine for containers — no servers to provision or patch, works under both ECS and EKS."},
            {"q": "What is the maximum execution duration for a single Lambda function invocation?",
             "options": ["5 minutes", "15 minutes", "1 hour", "Unlimited"],
             "answer": 1,
             "explanation": "Lambda is designed for short tasks; 15 minutes is the hard ceiling per invocation, which is why long-running processes belong on ECS/Fargate/EC2 instead."},
        ],
    },
    {
        "num": 12,
        "title": "Resilience and disaster recovery",
        "domain": "Resilience",
        "intro": "Planning for the worst case: how fast you recover, and how much data you can afford to lose.",
        "topics": [
            ("RTO and RPO",
             "RTO (Recovery Time Objective) is how long you can be down before it's a problem. RPO (Recovery Point "
             "Objective) is how much data you can afford to lose, measured in time (e.g., 'up to 1 hour of "
             "data'). Both drive which DR strategy you pick — tighter RTO/RPO costs more."),
            ("DR strategies: backup and restore, pilot light, warm standby, multi-site",
             "Backup and restore is cheapest, slowest to recover (hours). Pilot light keeps only the core (usually "
             "the database) running in the DR Region, scaled down, and you scale up compute when disaster "
             "strikes. Warm standby keeps a smaller-but-fully-functional copy running in the DR Region at all "
             "times, scaled up on failover. Multi-site (active-active) runs full production capacity in two "
             "Regions simultaneously — fastest recovery, most expensive."),
            ("Route 53 routing policies and health checks",
             "Simple (one resource), Weighted (split traffic by percentage), Latency-based (route to the Region "
             "with lowest latency for the user), Failover (primary/secondary, driven by health checks), "
             "Geolocation (route by the user's location), Geoproximity, Multi-value. Health checks let Route 53 "
             "detect a failed endpoint and stop routing to it."),
            ("CloudFront and Global Accelerator",
             "CloudFront is a CDN — caches content at edge locations to speed up content delivery. Global "
             "Accelerator routes traffic over AWS's private network backbone to the closest healthy endpoint — "
             "helps non-cacheable, dynamic, or non-HTTP traffic, unlike CloudFront which is HTTP(S)-focused and "
             "caching-focused."),
        ],
        "hands_on": [
            "Put CloudFront in front of your S3 static site.",
        ],
        "quiz": [
            {"q": "A company can tolerate losing at most 15 minutes of data, but needs to recover within 1 hour. What are they describing?",
             "options": ["RTO of 15 minutes, RPO of 1 hour", "RPO of 15 minutes, RTO of 1 hour", "Both are RTO", "Both are RPO"],
             "answer": 1,
             "explanation": "RPO is the tolerable data loss window; RTO is the tolerable downtime window. Here, 15 minutes of data loss is the RPO, and 1 hour recovery time is the RTO."},
            {"q": "A company wants the cheapest DR strategy and can tolerate several hours of downtime. What fits?",
             "options": ["Multi-site active-active", "Warm standby", "Backup and restore", "Pilot light"],
             "answer": 2,
             "explanation": "Backup and restore is the lowest-cost, slowest-recovery DR strategy — appropriate when RTO is measured in hours."},
            {"q": "What does a Route 53 failover routing policy require to work correctly?",
             "options": ["Weighted records", "A configured health check on the primary resource", "Geolocation records only", "CloudFront in front of it"],
             "answer": 1,
             "explanation": "Failover routing relies on Route 53 health checks to detect the primary's failure and redirect traffic to the secondary."},
            {"q": "An app has real-time, non-cacheable UDP traffic (like gaming or VoIP) that needs to reach the closest healthy endpoint over AWS's backbone. What fits best?",
             "options": ["CloudFront", "Global Accelerator", "Route 53 geolocation alone", "S3 Transfer Acceleration"],
             "answer": 1,
             "explanation": "Global Accelerator is built for non-HTTP, non-cacheable, latency-sensitive traffic, unlike CloudFront which is an HTTP(S) caching CDN."},
            {"q": "In the 'pilot light' DR strategy, what is typically kept running in the DR Region at all times?",
             "options": ["The full production fleet, fully scaled", "Just the core system (usually the database), scaled down", "Nothing at all", "Only the load balancer"],
             "answer": 1,
             "explanation": "Pilot light keeps only the essential core (e.g., a replicated database) running, letting you rapidly scale up compute on failover rather than starting from a blank slate."},
            {"q": "Which routing policy would you use to send 90% of traffic to a new version and 10% to the old version during a gradual rollout?",
             "options": ["Failover", "Weighted", "Geolocation", "Simple"],
             "answer": 1,
             "explanation": "Weighted routing splits traffic by percentage across multiple resources, ideal for gradual rollouts/canary releases."},
        ],
    },
    {
        "num": 13,
        "title": "Monitoring, data, migration",
        "domain": "Resilience",
        "intro": "How you observe a running system, audit who did what, and move data in and out of AWS.",
        "topics": [
            ("CloudWatch",
             "Metrics (numeric data over time, like CPU utilization), Logs (application/system log storage and "
             "search), Alarms (trigger an action, like an SNS notification, when a metric crosses a threshold)."),
            ("CloudTrail",
             "Records every API call made in your account (who did what, when) — the audit trail for "
             "security/compliance investigations. CloudWatch is for performance/health; CloudTrail is the "
             "who-did-what audit."),
            ("AWS Config",
             "Tracks configuration changes to your resources over time and can check them against compliance "
             "rules (e.g., 'flag any S3 bucket that becomes public')."),
            ("Trusted Advisor",
             "Automated checks across your account for cost savings, security gaps, performance, and service "
             "limits — like a built-in health inspector."),
            ("Systems Manager",
             "A suite of tools for operating your fleet — Session Manager, Run Command (execute commands across "
             "many instances), Patch Manager, and more."),
            ("Kinesis, Athena, Glue",
             "Kinesis ingests and processes real-time streaming data (like clickstreams or IoT data). Athena runs "
             "SQL queries directly against data sitting in S3, no database needed. Glue is a managed ETL "
             "(extract-transform-load) service that discovers, cleans, and moves data between stores."),
            ("DataSync, Storage Gateway, Snow family, DMS",
             "DataSync automates online transfer of large datasets between on-prem and AWS (or between AWS "
             "stores). Storage Gateway bridges on-prem applications to AWS storage as if it were local. The Snow "
             "family (Snowball, Snowcone) are physical devices for shipping huge amounts of data when the network "
             "is too slow or expensive. DMS (Database Migration Service) migrates databases to AWS with minimal "
             "downtime, and can even convert between engines with the Schema Conversion Tool."),
        ],
        "hands_on": [
            "Set a CloudWatch alarm that triggers an SNS email when a metric crosses a threshold.",
        ],
        "quiz": [
            {"q": "You need to know exactly which IAM user deleted a specific S3 bucket last Tuesday. Where do you look?",
             "options": ["CloudWatch", "CloudTrail", "Trusted Advisor", "AWS Config"],
             "answer": 1,
             "explanation": "CloudTrail is the audit log of every API call, including who made it and when — exactly the 'who did what' tool."},
            {"q": "A company wants to be automatically flagged whenever an S3 bucket's configuration changes to become public. What service fits?",
             "options": ["CloudWatch Logs", "AWS Config", "Kinesis", "Athena"],
             "answer": 1,
             "explanation": "Config tracks configuration changes over time and can evaluate them against compliance rules you define."},
            {"q": "You have huge volumes of data in on-premises storage and need to migrate it to AWS, but your internet link is too slow to do it in a reasonable time. What should you use?",
             "options": ["DataSync", "The Snow family", "Storage Gateway", "DMS"],
             "answer": 1,
             "explanation": "Snowball/Snowcone are physical devices meant exactly for large data transfers where the network isn't fast enough."},
            {"q": "What lets you run SQL queries directly against files sitting in S3, without standing up a database?",
             "options": ["Glue", "Athena", "Kinesis", "RDS"],
             "answer": 1,
             "explanation": "Athena is a serverless query service specifically built to run SQL over data already in S3."},
            {"q": "What is Trusted Advisor best described as?",
             "options": ["A log storage service", "An automated set of checks for cost, security, performance, and limits across your account", "A database migration tool", "A real-time streaming service"],
             "answer": 1,
             "explanation": "Trusted Advisor scans your account and surfaces recommendations across several categories automatically."},
            {"q": "You need to migrate an on-prem MySQL database to RDS with minimal downtime. What service is purpose-built for this?",
             "options": ["DataSync", "Database Migration Service", "Storage Gateway", "Glue"],
             "answer": 1,
             "explanation": "DMS is specifically designed for database migrations, including ongoing replication to minimize cutover downtime."},
        ],
    },
    {
        "num": 14,
        "title": "Cost optimization",
        "domain": "Cost",
        "intro": "The smallest-weighted domain, but full of small factual details the exam likes to test directly.",
        "topics": [
            ("On-Demand, Reserved, Savings Plans, Spot, Dedicated Hosts",
             "On-Demand: pay as you go, most flexible, most expensive. Reserved Instances: commit to a specific "
             "instance type/Region for 1-3 years for a discount. Savings Plans: commit to a $/hour spend (more "
             "flexible across instance families/sizes) for a similar discount to RIs. Spot: spare capacity at up "
             "to ~90% off, can be reclaimed. Dedicated Hosts: a physical server billed to you alone, for "
             "licensing/compliance needs (e.g., bring-your-own-license software)."),
            ("S3 Intelligent-Tiering",
             "Automatically moves objects between access tiers based on usage, avoiding the need to manually pick "
             "a storage class and avoiding retrieval fees for infrequent access."),
            ("Data transfer costs",
             "Data transfer IN to AWS is generally free. Data transfer OUT to the internet costs money and is "
             "often the 'hidden' cost on the exam. Transfer between AZs in the same Region also costs money; "
             "transfer within the same AZ is free. This exact detail shows up often."),
            ("Cost Explorer, Budgets",
             "Cost Explorer visualizes and analyzes your spending over time, and can forecast future costs. "
             "Budgets lets you set spending thresholds and get alerted (or even trigger an action) when you're "
             "projected to exceed them."),
        ],
        "hands_on": [
            "Open Cost Explorer on your own account and find your single biggest cost line item.",
        ],
        "quiz": [
            {"q": "Which of these typically costs money?",
             "options": ["Data transfer into AWS", "Data transfer out to the internet", "Transfer within the same Availability Zone", "None of these cost money"],
             "answer": 1,
             "explanation": "Inbound data transfer and same-AZ transfer are generally free; outbound-to-internet transfer is the one that usually carries a real cost — a frequent exam trap."},
            {"q": "A company has steady, predictable EC2 usage for the next 3 years and wants the maximum possible discount, and is fine locking into specific instance families. What should they buy?",
             "options": ["On-Demand", "Reserved Instances", "Spot Instances", "Dedicated Hosts"],
             "answer": 1,
             "explanation": "RIs offer some of the deepest discounts for steady, predictable workloads with a multi-year commitment."},
            {"q": "A company needs the discount of a Reserved Instance but wants the flexibility to shift spend across different instance families and even other services like Fargate. What fits better?",
             "options": ["Reserved Instances", "Savings Plans", "Spot Instances", "Dedicated Hosts"],
             "answer": 1,
             "explanation": "Savings Plans commit to a dollar amount per hour rather than a specific instance type, giving more flexibility than RIs while still getting a discount."},
            {"q": "What does S3 Intelligent-Tiering primarily save you from doing?",
             "options": ["Manually managing IAM policies", "Manually choosing and switching storage tiers as access patterns change", "Setting up versioning", "Creating lifecycle rules for security"],
             "answer": 1,
             "explanation": "Intelligent-Tiering automates the tier-switching that lifecycle rules would otherwise require you to configure manually."},
            {"q": "What's the difference between Cost Explorer and Budgets?",
             "options": ["They are the same tool with different names", "Cost Explorer analyzes/visualizes past and forecasted spend; Budgets alerts you when spend is projected to cross a threshold you set", "Budgets is for IAM cost tracking only", "Cost Explorer can trigger automatic account shutdowns"],
             "answer": 1,
             "explanation": "Cost Explorer is analysis/visualization; Budgets is proactive alerting (and optionally actions) against thresholds you define."},
            {"q": "A licensing requirement says certain software must run on a physical server dedicated entirely to one customer. What purchase option satisfies this?",
             "options": ["Reserved Instances", "Dedicated Hosts", "Savings Plans", "Spot Instances"],
             "answer": 1,
             "explanation": "Dedicated Hosts give you an entire physical server, which matters for certain per-socket/per-core licensing terms."},
        ],
    },
    {
        "num": 15,
        "title": "Practice exams",
        "domain": "Exam prep",
        "intro": "No new AWS content this week — just full timed practice exams and disciplined review of what you got wrong.",
        "topics": [
            ("How to review a practice exam properly",
             "Spend more time reviewing than testing. For every wrong answer, write one sentence: why was your "
             "answer wrong, and why was the correct one better? This turns a graded test into a targeted study "
             "list, and is far more valuable than just noting the score."),
            ("Simulate real exam conditions",
             "Two full timed practice exams this week: 130 minutes, no notes, one sitting — so the format itself "
             "isn't a surprise on exam day."),
        ],
        "hands_on": [
            "Take two full timed practice exams.",
            "Write a one-sentence review note for every question you missed.",
        ],
        "quiz": [
            {"q": "You have 130 minutes for 65 questions. Roughly how much time per question should you budget?",
             "options": ["About 30 seconds", "About 2 minutes", "About 10 minutes", "There's no time limit"],
             "answer": 1,
             "explanation": "130 minutes divided by 65 questions is about 2 minutes each — useful for pacing so you don't run out of time."},
            {"q": "After finishing a timed practice exam, what should you spend the most time on?",
             "options": ["Immediately retaking it", "Reviewing every wrong answer and writing why", "Moving on to a new topic entirely", "Only checking your final score"],
             "answer": 1,
             "explanation": "The review — understanding why an answer was wrong and why the correct one was better — is where the actual learning happens, more than the raw score."},
            {"q": "A question describes a scenario where two answers technically 'work.' What does this usually mean?",
             "options": ["The question is broken", "You must choose the best answer given the stated constraints (cost, security, effort), not just any working one", "Both answers should be selected", "Skip the question"],
             "answer": 1,
             "explanation": "SAA-C03 is built around 'best fit for the constraints given,' not simple factual recall — this is explicitly the exam's design."},
            {"q": "If you score around 50-60% on your first timed practice exam at week 15, what should you do?",
             "options": ["Panic and delay the exam indefinitely", "Use the wrong-answer review to target the remaining study time", "Retake the exact same exam repeatedly without reviewing", "Switch certifications"],
             "answer": 1,
             "explanation": "A moderate score this late is a signal for where to focus, not a reason to abandon the timeline — the plan builds in this exact checkpoint."},
        ],
    },
    {
        "num": 16,
        "title": "Final review and book it",
        "domain": "Exam prep",
        "intro": "The last week is about consolidation and forcing a real deadline, not learning new material.",
        "topics": [
            ("Re-read your own wrong-answer notes",
             "Your own notes from weeks 8 and 15 are more targeted to your actual gaps than any generic review "
             "material."),
            ("Skim service comparison sheets",
             "Quick-reference sheets (S3 storage classes, RDS vs Aurora vs DynamoDB, ALB vs NLB, etc.) are for "
             "final recall, not first-time learning — if something on the sheet feels unfamiliar, that's a sign "
             "to go back to that week's material, not just memorize the sheet."),
            ("Book the exam",
             "Should already be booked by week 12; if not, book it now, and set the date at the end of this week."),
            ("The readiness signal",
             "You are ready when you score 80%+ on new (unseen) practice exams two times in a row — not on ones "
             "you've memorized."),
        ],
        "hands_on": [
            "Book the exam if you haven't already.",
            "Do one final skim of comparison sheets and your wrong-answer notes.",
        ],
        "quiz": [
            {"q": "What is the readiness signal the plan defines for 'you are ready to take the real exam'?",
             "options": ["Finishing all 16 weeks regardless of score", "Scoring 80%+ on unseen practice exams, twice in a row", "Watching all course videos twice", "Memorizing every AWS service"],
             "answer": 1,
             "explanation": "The plan explicitly defines readiness as a repeatable 80%+ score on exams you haven't already memorized, not just completing the calendar."},
            {"q": "Why should you book the exam date well before you feel 'fully ready'?",
             "options": ["Because AWS requires it", "Because a plan with no real date tends to quietly slip and stretch out much longer", "Because the price increases if you wait", "Because AWS limits how many times you can book"],
             "answer": 1,
             "explanation": "The plan calls out that without a concrete booked date, a 16-week plan can quietly become a 40-week plan — a real deadline forces the pace."},
            {"q": "What is the best use of a service comparison sheet (e.g., 'RDS vs Aurora vs DynamoDB') in week 16?",
             "options": ["Learning these services for the first time", "A quick final-recall refresher, not first-time learning", "Replacing the earlier weeks' study entirely", "Something to skip, since it's not on the exam"],
             "answer": 1,
             "explanation": "Comparison sheets work best for reinforcing material you already studied — if something on it feels new, that's a signal to revisit that week's content specifically."},
            {"q": "You've completed week 16, but you consistently score 65-70% on new practice exams. What should you do?",
             "options": ["Take the real exam anyway on schedule", "Extend review time until you hit the 80%+ readiness bar consistently", "Rebook for a random earlier date", "Give up on the certification"],
             "answer": 1,
             "explanation": "The 80%+-twice-in-a-row signal is the actual gate, not the calendar date — if you're not there yet, the plan is to keep reviewing rather than sit the exam underprepared."},
        ],
    },
]

DOMAIN_COLORS = {
    "Foundations": "#6b7280",
    "Security": "#dc2626",
    "Resilience": "#2563eb",
    "Cost": "#059669",
    "Exam prep": "#7c3aed",
}
