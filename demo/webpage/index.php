<?php
$platform = $_ENV['PLATFORM'];
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link href="style.css" rel="stylesheet">
    <title>Nutanix</title>
</head>

<body>

    <main class="main">
        <div class="container">
            <div class="row">
                <div class="col-lg-12">
                    <h1>Nutanix Hybrid Cloud Application</h1>
                </div>
            </div>
            <div class="row">
                <div class="mt-5 mb-5 col-lg-6">
                    <p class="text-center">
                        <a href="#" class="btn btn-md btn-secondary">Host: <?php echo gethostname(); ?></a>
                    </p>
                </div>
                <div class="mt-5 mb-5 col-lg-6">
                    <p class="text-center">
                        <a href="#" class="<?php echo $platform ?> btn btn-md btn-secondary">Cloud: <?php echo $platform ?></a>
                    </p>
                </div>
            </div>
            <div class="row">
                <div class="mt-5 mb-5 col-lg-12">
                    <img class="img-fluid" src="nutanix_hybrid_cloud.png">
                </div>
            </div>
        </div>
    </main>
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col">
                    <a href="https://github.com/pipoe2h" target="_blank">Designed by Jose Gomez</a>
                </div>
                    <div class="col">
                        <a href="https://nutanix.com" target="_blank"><img class="img-fluid" src="nutanix_logo.png"></a>
                    </div>
                <div class="col">
                    <a class="float-right" href="<?php echo 'http://' .getenv('CALM_LB'). ':8080/stats'; ?>" target="_blank">Load Balancer</a>
                </div>
            </div>
        </div>
    </footer>


    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous">
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
        integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous">
    </script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
        integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous">
    </script>
</body>

</html>