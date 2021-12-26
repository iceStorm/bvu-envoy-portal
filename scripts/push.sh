echo "Creating requirements.txt..."
./freeze.sh
echo "Done."
echo

read -p "Enter commit message: " commitMessage


git add --all
git commit -m "$commitMessage"
git push origin master
