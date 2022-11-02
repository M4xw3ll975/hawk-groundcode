<?php
//save the uploaded file
echo move_uploaded_file(
    $_FILES['file']['tmp_name'],
     'path.gpx'
) ? 'UPLOAD DONE' : 'UPLOAD FAILED';