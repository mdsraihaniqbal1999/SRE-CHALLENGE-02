import json
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class S3BucketOptimizer:
    def __init__(self, bucket_file='buckets.json'):
        """
        Initialize the S3 Bucket Optimizer with bucket data
        
        Args:
            bucket_file (str): Path to the JSON file containing bucket information
        """
        with open(bucket_file, 'r') as f:
            self.buckets = json.load(f)['buckets']
        
        # Current date for aging calculations (simulated as the latest bucket creation date)
        self.current_date = max(datetime.strptime(bucket['createdOn'], '%Y-%m-%d') for bucket in self.buckets)

    def print_bucket_summary(self):
        """
        Print a summary of each bucket with key metadata
        """
        print("\n--- BUCKET SUMMARY ---")
        for bucket in self.buckets:
            print(f"Name: {bucket['name']}")
            print(f"  Region: {bucket['region']}")
            print(f"  Size: {bucket['sizeGB']} GB")
            print(f"  Versioning: {'Enabled' if bucket['versioning'] else 'Disabled'}")
            print(f"  Created On: {bucket['createdOn']}")
            print("---")

    def identify_large_unused_buckets(self, size_threshold=80, age_threshold=90):
        """
        Identify large buckets that have been unused for a significant period
        
        Args:
            size_threshold (int): Minimum size in GB to consider
            age_threshold (int): Minimum days of inactivity
        
        Returns:
            list: Buckets meeting the criteria
        """
        large_unused_buckets = []
        for bucket in self.buckets:
            bucket_age = (self.current_date - datetime.strptime(bucket['createdOn'], '%Y-%m-%d')).days
            
            if (bucket['sizeGB'] > size_threshold and 
                bucket_age > age_threshold):
                large_unused_buckets.append(bucket)
        
        return large_unused_buckets

    def generate_cost_report(self):
        """
        Generate a cost report grouped by region and department
        
        Assumes a base cost of $0.023 per GB per month
        """
        COST_PER_GB_PER_MONTH = 0.023
        
        cost_report = {}
        
        for bucket in self.buckets:
            region = bucket['region']
            team = bucket['tags'].get('team', 'Unknown')
            size = bucket['sizeGB']
            
            # Calculate monthly cost
            monthly_cost = size * COST_PER_GB_PER_MONTH
            
            if region not in cost_report:
                cost_report[region] = {}
            
            if team not in cost_report[region]:
                cost_report[region][team] = {
                    'total_size': 0,
                    'total_cost': 0,
                    'buckets': []
                }
            
            cost_report[region][team]['total_size'] += size
            cost_report[region][team]['total_cost'] += monthly_cost
            cost_report[region][team]['buckets'].append({
                'name': bucket['name'],
                'size': size,
                'monthly_cost': monthly_cost
            })
        
        return cost_report

    def identify_deletion_candidates(self, size_threshold=100, inactivity_days=20):
        """
        Identify buckets for potential deletion or archival
        
        Args:
            size_threshold (int): Minimum size in GB to consider for deletion
            inactivity_days (int): Maximum days of inactivity before considering deletion
        
        Returns:
            dict: Buckets to delete or archive
        """
        deletion_candidates = {
            'delete': [],
            'archive_to_glacier': []
        }
        
        for bucket in self.buckets:
            bucket_age = (self.current_date - datetime.strptime(bucket['createdOn'], '%Y-%m-%d')).days
            
            if bucket['sizeGB'] > size_threshold and bucket_age > inactivity_days:
                # Prioritize deletion for production buckets with no current policies
                if not bucket['policies'] and bucket['tags'].get('environment') == 'prod':
                    deletion_candidates['delete'].append(bucket)
                else:
                    deletion_candidates['archive_to_glacier'].append(bucket)
        
        return deletion_candidates

    def visualize_cost_distribution(self, cost_report):
        """
        Create a pie chart of cost distribution by region
        """
        plt.figure(figsize=(10, 6))
        
        # Aggregate costs by region
        region_costs = {region: sum(team_data['total_cost'] for team_data in region_teams.values())
                        for region, region_teams in cost_report.items()}
        
        plt.pie(list(region_costs.values()), 
                labels=list(region_costs.keys()), 
                autopct='%1.1f%%')
        plt.title('S3 Storage Cost Distribution by Region')
        plt.tight_layout()
        plt.savefig('region_cost_distribution.png')
        plt.close()

    def run_optimization_analysis(self):
        """
        Comprehensive S3 bucket optimization analysis
        """
        # 1. Print Bucket Summary
        self.print_bucket_summary()
        
        # 2. Identify Large Unused Buckets
        large_unused = self.identify_large_unused_buckets()
        print("\n--- LARGE UNUSED BUCKETS ---")
        for bucket in large_unused:
            print(f"Bucket: {bucket['name']}, Size: {bucket['sizeGB']} GB, Region: {bucket['region']}")
        
        # 3. Generate Cost Report
        cost_report = self.generate_cost_report()
        print("\n--- COST REPORT ---")
        for region, teams in cost_report.items():
            print(f"\nRegion: {region}")
            for team, data in teams.items():
                print(f"  Team: {team}")
                print(f"    Total Size: {data['total_size']} GB")
                print(f"    Monthly Cost: ${data['total_cost']:.2f}")
        
        # 4. Identify Deletion Candidates
        deletion_candidates = self.identify_deletion_candidates()
        print("\n--- DELETION CANDIDATES ---")
        print("Buckets to Delete:")
        for bucket in deletion_candidates['delete']:
            print(f"  {bucket['name']} (Size: {bucket['sizeGB']} GB)")
        
        print("\nBuckets to Archive to Glacier:")
        for bucket in deletion_candidates['archive_to_glacier']:
            print(f"  {bucket['name']} (Size: {bucket['sizeGB']} GB)")
        
        # 5. Visualize Cost Distribution
        self.visualize_cost_distribution(cost_report)

# Execute the optimization analysis
if __name__ == "__main__":
    optimizer = S3BucketOptimizer()
    optimizer.run_optimization_analysis()
