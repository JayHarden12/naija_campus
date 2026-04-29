# Naija Campus Bot - Current State Assessment
Date: [20/04/2026]
Assessed by: Margaret

## Files Found
mlb_classes.pkl          20/04/2026             1KB
model.safetensors        20/04/2026             261,673KB
Master_Dataset           20/04/2026             5,414KB
Master_Dataset_Labeled   20/04/2026             5,570KB
response_bank            20/04/2026             110KB
config                   20/04/2026             3KB
tokenizer                20/04/2026             695KB
tokenizer_config         20/04/2026             1KB

## What's working
All documents are working as they should, they are currently in the process of being merged into the main branch of the repository on Github
remote: error: File model.safetensors is 255.54 MB; this exceeds GitHub's file size limit of 100.00 MB
ChatGPT suggested; Install Git LFS:

git lfs install
git lfs track "*.safetensors"

Then:

git add .gitattributes
git add data/models/model.safetensors
git commit -m "Track model with Git LFS"
git push origin folders-and-resources
but I went with option 1 which was to remove the file from pushing to git since the file is on our shared Google drive