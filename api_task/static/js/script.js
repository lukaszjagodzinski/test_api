$(document).ready(function() {
    // Attach a click event to a link with the class 'fetchLink'
    $('.fetchLink').click(function(event) {
        event.preventDefault(); // Prevent the default link behavior

        // Extract the href attribute from the clicked link
        var url = $(this).attr('href');

        // Make an asynchronous request to the specified URL
        fetchData(url);
    });

    function fetchData(url) {
        $.ajax({
            url: url,
            method: 'GET',
            dataType: 'json',
            success: function(data) {
                displayData(data);
            },
            error: function(error) {
                console.error('There was a problem with the fetch operation:', error);
            }
        });
    }

    function displayData(data) {
        // Replace this with logic to display the data on the page
        $('#result').html(JSON.stringify(data, null, 2));
    }
});