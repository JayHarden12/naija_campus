#!/usr/bin/env python3
"""
Relabel Master_Dataset_Labeled.csv: 122 labels → 52 classes (middle path).
Reads the CSV, applies the merge map, deduplicates labels per row, writes back.
"""

import csv
import sys
from collections import Counter

MERGE_MAP = {
    # ── Into NEW bucket: therapy_process ──
    'therapy_process_inquiry': 'therapy_process',
    'therapy_inquiry': 'therapy_process',
    'therapy_effectiveness_doubt': 'therapy_process',
    'seeking_counseling': 'therapy_process',
    'therapist_misconduct': 'therapy_process',
    'therapy_boundaries': 'therapy_process',
    'counselor_skills_inquiry': 'therapy_process',
    'therapist_background_inquiry': 'therapy_process',
    'sharing_treatment_info': 'therapy_process',

    # ── Into NEW bucket: health_anxiety ──
    'health_medical_anxiety': 'health_anxiety',
    'condition_clarification': 'health_anxiety',
    'chronic_illness': 'health_anxiety',
    'child_health_concern': 'health_anxiety',

    # ── Into NEW bucket: body_image ──
    'body_image_insecurities': 'body_image',
    'eating_disorder': 'body_image',

    # ── Into NEW bucket: spiritual_religious_conflict ──
    'spiritual_religious_guilt': 'spiritual_religious_conflict',

    # ── Into NEW bucket: guilt_shame ──
    'guilt_remorse': 'guilt_shame',
    'empathy_distress': 'guilt_shame',

    # ── Into NEW bucket: relationship_dynamics ──
    'relationship_conflict': 'relationship_dynamics',
    'communication_conflict': 'relationship_dynamics',
    'boundary_setting_issues': 'relationship_dynamics',
    'relationship_ending_dilemma': 'relationship_dynamics',
    'infidelity': 'relationship_dynamics',
    'partner_negative_influence': 'relationship_dynamics',
    'marital_conflict': 'relationship_dynamics',
    'reconnection_dilemma': 'relationship_dynamics',
    'relationship_dependency': 'relationship_dynamics',

    # ── Into NEW bucket: intimacy_concerns ──
    'relationship_intimacy_concern': 'intimacy_concerns',
    'relationship_intimacy_issues': 'intimacy_concerns',
    'sexual_intimacy_issues': 'intimacy_concerns',

    # ── Into NEW bucket: identity_gender_sexuality ──
    'sexuality_identity_confusion': 'identity_gender_sexuality',
    'coming_out_dilemma': 'identity_gender_sexuality',
    'gender_identity_questioning': 'identity_gender_sexuality',
    'gender_dysphoria_distress': 'identity_gender_sexuality',
    'gender_expression': 'identity_gender_sexuality',
    'sexuality_gender_expression': 'identity_gender_sexuality',
    'gender_transition_inquiry': 'identity_gender_sexuality',
    'sexuality_inquiry': 'identity_gender_sexuality',

    # ── Into NEW bucket: seeking_normalization_validation ──
    'seeking_normalization': 'seeking_normalization_validation',
    'seeking_validation': 'seeking_normalization_validation',

    # ── Into NEW bucket: understanding_symptoms (name stays, just promoted) ──
    'understanding_symptoms': 'understanding_symptoms',

    # ── Into NEW bucket: helping_others ──
    'seeking_help_for_other': 'helping_others',
    'third_party_concern': 'helping_others',

    # ── Into NEW bucket: neurodivergence ──
    'neurodivergence_adhd': 'neurodivergence',
    'learning_disability': 'neurodivergence',

    # ── Into NEW bucket: severe_symptom_referral ──
    'auditory_hallucinations': 'severe_symptom_referral',
    'hearing_voices': 'severe_symptom_referral',
    'reality_distortion': 'severe_symptom_referral',
    'dissociative_amnesia': 'severe_symptom_referral',
    'intrusive_thoughts': 'severe_symptom_referral',
    'ptsd': 'severe_symptom_referral',
    'bipolar_disorder': 'severe_symptom_referral',
    'violent_urges': 'severe_symptom_referral',
    'involuntary_commitment': 'severe_symptom_referral',

    # ── Into NEW bucket: pregnancy_reproductive ──
    'unplanned_pregnancy_scare': 'pregnancy_reproductive',

    # ── Into EXISTING buckets ──
    'abusive_relationship_dilemma': 'crisis_abuse_trauma',
    'existential_anxiety': 'general_anxiety',
    'relationship_anxiety': 'general_anxiety',
    'logistical_crisis': 'general_anxiety',
    'legal_advice_seeking': 'general_anxiety',
    'ethical_legal_inquiry': 'general_anxiety',
    'social_anxiety': 'loneliness_isolation',
    'culture_shock': 'loneliness_isolation',
    'future_career_anxiety': 'exam_anxiety',
    'compulsive_behavior_issue': 'substance_abuse_addiction',
    'social_media_phone_addiction': 'substance_abuse_addiction',
    'sexual_addiction': 'substance_abuse_addiction',
    'identity_disturbance': 'low_self_esteem',
    'imposter_syndrome': 'low_self_esteem',
    'childcare_behavior_issue': 'family_conflict',
    'parenting_dilemma': 'family_conflict',
    'family_intervention_inquiry': 'family_conflict',
    'parental_attachment_concern': 'family_conflict',
    'parenthood_decision_dilemma': 'family_conflict',
    'inner_turmoil': 'sadness_depression',
    'emotional_numbness': 'sadness_depression',
    'emotional_dysregulation': 'anger_irritability',
    'rebellious_behavior': 'anger_irritability',
    'general_stress': 'fatigue_burnout',
    'workplace_stress': 'fatigue_burnout',
    'life_management_stress': 'fatigue_burnout',
    'event_planning_stress': 'fatigue_burnout',
    'professional_background_inquiry': 'bot_identity',
    'friend_loss_grief': 'family_loss_grief',
    'romantic_crush': 'relationship_heartbreak',
    'romantic_interest_stress': 'relationship_heartbreak',
    'dating_advice': 'relationship_heartbreak',
    'relationship_inquiry': 'relationship_heartbreak',
}

INPUT_FILE = 'data/Master_Dataset_Labeled.csv'
OUTPUT_FILE = 'data/Master_Dataset_Labeled.csv'


def relabel_row(intents_str):
    """Apply merge map to a comma-separated intents string."""
    if not intents_str.strip():
        return intents_str

    labels = [l.strip() for l in intents_str.split(',') if l.strip()]
    new_labels = []
    seen = set()
    for label in labels:
        mapped = MERGE_MAP.get(label, label)
        if mapped not in seen:
            new_labels.append(mapped)
            seen.add(mapped)
    return ', '.join(new_labels)


def main():
    # Read all rows
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Read {len(rows)} rows from {INPUT_FILE}")

    # Count labels before
    before_labels = Counter()
    for row in rows:
        for l in [x.strip() for x in row.get('intents', '').split(',') if x.strip()]:
            before_labels[l] += 1
    print(f"Labels BEFORE: {len(before_labels)} unique")

    # Apply relabeling
    rows_modified = 0
    for row in rows:
        old = row.get('intents', '')
        new = relabel_row(old)
        if new != old:
            rows_modified += 1
        row['intents'] = new

    # Count labels after
    after_labels = Counter()
    for row in rows:
        for l in [x.strip() for x in row.get('intents', '').split(',') if x.strip()]:
            after_labels[l] += 1
    print(f"Labels AFTER: {len(after_labels)} unique")
    print(f"Rows modified: {rows_modified}")

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nWrote {len(rows)} rows to {OUTPUT_FILE}")

    # Print final label distribution
    print(f"\n{'='*60}")
    print(f"FINAL LABEL DISTRIBUTION ({len(after_labels)} classes)")
    print(f"{'='*60}")
    for label, count in after_labels.most_common():
        print(f"  {label}: {count}")

    # Verify no unmapped extra labels remain
    expected_labels = set([
        'academic_failure', 'academic_workload', 'anger_irritability',
        'appetite_changes', 'bot_capabilities', 'bot_identity',
        'bullying_harassment', 'casual_goodbye', 'casual_greeting',
        'concentration_focus', 'crisis_abuse_trauma', 'crisis_self_harm',
        'crisis_suicide_ideation', 'exam_anxiety', 'family_conflict',
        'family_loss_grief', 'family_pressure', 'fatigue_burnout',
        'financial_stress', 'food_insecurity', 'friendship_conflict',
        'general_anxiety', 'housing_accommodation', 'lack_of_motivation',
        'lecturer_conflict', 'loneliness_isolation', 'low_self_esteem',
        'panic_attack', 'paranoia_trust_issues', 'peer_pressure',
        'project_thesis_stress', 'relationship_heartbreak',
        'sadness_depression', 'seeking_coping_advice', 'sleep_insomnia',
        'substance_abuse_addiction', 'user_appreciation', 'user_frustration',
        # 14 new buckets
        'therapy_process', 'health_anxiety', 'relationship_dynamics',
        'seeking_normalization_validation', 'intimacy_concerns',
        'body_image', 'guilt_shame', 'spiritual_religious_conflict',
        'helping_others', 'identity_gender_sexuality',
        'understanding_symptoms', 'neurodivergence',
        'severe_symptom_referral', 'pregnancy_reproductive',
    ])

    actual_labels = set(after_labels.keys())
    unexpected = actual_labels - expected_labels
    missing_new = (expected_labels - actual_labels) - {'casual_goodbye', 'casual_greeting', 'food_insecurity', 'project_thesis_stress'}

    if unexpected:
        print(f"\n⚠️  UNEXPECTED labels found: {unexpected}")
    else:
        print(f"\n✅ No unexpected labels — all mapped correctly")

    if missing_new:
        print(f"⚠️  Expected labels NOT found in data: {missing_new}")

    return 0 if not unexpected else 1


if __name__ == '__main__':
    sys.exit(main())
