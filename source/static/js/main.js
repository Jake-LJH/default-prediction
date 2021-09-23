$(document).ready(function() {
  $('#predicted_table').DataTable({
    "scorllX": true,
    "scrollY": 500
  });
  $('.dataTables_length').addClass('bs-select');
});

$(".custom-file-input").on("change", function() {
  var fileName = $(this).val().split("\\").pop();
  $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});
