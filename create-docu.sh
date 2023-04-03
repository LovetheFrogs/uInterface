cargo doc --no-deps
rm -rf ./docs
touch target/doc/index.html
echo "<meta http-equiv\"refresh\" content=\"0; url=build_wheel\">" > target/doc/index.html
cp -r target/doc ./docs
