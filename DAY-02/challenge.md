# Day 2 Challenge: S3 Bucket Metadata Management and Cost Optimization

## Hello Learners,

Welcome back to the **DevOps SRE Daily Challenge!** 🎉

Today, you’ll dive into **cloud storage optimization** and **scripting**, focusing on managing **S3 bucket metadata** and identifying cost-saving opportunities. Using a provided JSON file (`buckets.json`), you will create a Python script to analyze, modify, and optimize S3 bucket metadata.

---

## Requirements

Using the provided JSON file, implement the following:

1. **Print a summary of each bucket:**
   - Name
   - Region
   - Size (in GB)
   - Versioning status

2. **Identify buckets larger than 80 GB** from every region which are unused for 90+ days.

3. **Generate a cost report:**
   - Total S3 bucket cost grouped by region and department.
   - Highlight buckets with:
     - **Size > 50 GB:** Recommend cleanup operations.
     - **Size > 100 GB and not accessed in 20+ days:** Add these to a deletion queue.

4. **Provide a final list of buckets to delete (from the deletion queue):**
   - For archival candidates, suggest moving to Glacier.

---

## Why This Matters

**Cost efficiency** is a cornerstone of cloud-native practices. Today’s challenge will teach you how to:
- Analyze and optimize cloud resources.
- Automate cleanup operations.
- Reduce costs.

These skills are essential for modern **DevOps roles**.

---

## Submission Guidelines

1. **GitHub Repository:** Upload your script and `buckets.json`.
2. **Documentation:** Include a `README.md` explaining your approach, challenges faced, and key learnings.
3. **Share Your Progress:** Post your experience with hashtags:
   - **#getfitwithsagar, #SRELife, #DevOpsForAll.**

---

## Take Action and Save Costs!

Every script you write today brings you closer to mastering **cost optimization in DevOps**.

---

## Good luck!

Best regards,  
**Sagar Utekar**

