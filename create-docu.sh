#!/bin/bash
cargo doc --document-private-items --no-deps
rm -rf ./docs
touch target/doc/index.html
echo "<script>
        var timer = setTimeout(function() {
            window.location='u_interface/index.html'
        }, 0);
 </script>
" > target/doc/index.html
cp -r target/doc ./docs
