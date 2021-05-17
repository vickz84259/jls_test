function update_quantity(event) {
    const button = event.target;
    const input_element = document.getElementById(button.dataset.id);

    const new_value = input_element.value;
    const core_number = button.dataset.product;

    window.location.assign(
        `https://jls.slick.co.ke/update/${core_number}/${button.dataset.id}/${new_value}`);
}

const buttons = document.querySelectorAll('button');
buttons.forEach(function(button) {
  button.onclick = update_quantity;
});
