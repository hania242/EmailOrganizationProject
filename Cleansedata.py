import pandas as pd

def super_strict_email_cleaning(csv_file):
    """Ultra-strict cleaning for genuine email organization problems only"""
    
    df = pd.read_csv(csv_file)
    print(f"Starting with {len(df)} posts")
    
    genuine_posts = []
    
    for i, row in df.iterrows():
        title = str(row['title']).lower()
        text = str(row['text']).lower() if pd.notna(row['text']) else ""
        combined = title + " " + text
        
        # MUST be specifically about email organization (very strict)
        email_org_specific = [
            "organize email", "organize gmail", "email organization", "gmail organization",
            "inbox organization", "cluttered inbox", "messy inbox", "inbox management",
            "too many emails", "email overload", "overwhelmed by email",
            "can't find email", "lost email", "search email", "find email",
            "email productivity", "inbox zero", "manage email", "email management",
            "sort email", "categorize email", "filter email", "email chaos",
            "unread email", "thousands of email", "hundreds of email"
        ]
        
        has_specific_problem = any(phrase in combined for phrase in email_org_specific)
        
        # EXCLUDE anything that's clearly not about email organization
        exclude_completely = [
            "eating the frog", "productivity method", "asking myself", "rewired my life",
            "angry email", "never send", "amazon smile", "meal plan", "recipe",
            "job interview", "resume", "career", "dating", "relationship",
            "apartment", "rent", "landlord", "turkey", "thanksgiving",
            "wasn't unproductive", "functional human", "task management system",
            "habit tracker", "planner", "productivity hack", "time blocking",
            "pomodoro", "focus session", "getting things done"
        ]
        
        is_excluded = any(phrase in combined for phrase in exclude_completely)
        
        # Additional check: title must contain email/gmail/inbox
        title_has_email = any(word in title for word in ['email', 'gmail', 'inbox', 'mail'])
        
        # Keep only if: specific org problem + not excluded + email in title
        if has_specific_problem and not is_excluded and title_has_email:
            genuine_posts.append(row)
            print(f"KEEP: \"{row['title'][:60]}...\" ({row['score']} upvotes)")
        else:
            print(f"DELETE: \"{row['title'][:60]}...\"")
    
    # Save super-cleaned data
    cleaned_df = pd.DataFrame(genuine_posts)
    output_file = 'super_clean_email_posts.csv'
    cleaned_df.to_csv(output_file, index=False)
    
    print(f"\nRESULTS:")
    print(f"Original: {len(df)} posts")
    print(f"Super-cleaned: {len(cleaned_df)} posts")
    print(f"Saved to: {output_file}")
    
    if len(cleaned_df) > 0:
        print(f"\nTOP POSTS IN CLEANED DATA:")
        top_posts = cleaned_df.nlargest(5, 'score')
        for i, row in top_posts.iterrows():
            print(f"• \"{row['title']}\" ({row['score']} upvotes)")
    
    return output_file

# Run super strict cleaning
if __name__ == "__main__":
    super_strict_email_cleaning('reddit_email_raw_data_20250827_0840.csv')