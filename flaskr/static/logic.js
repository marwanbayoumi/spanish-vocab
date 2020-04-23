selectTable()

function selectTable() {

    let selector = document.querySelector('#selector')

    for (opt of selector) {

        if (opt.value === selector.dataset.table) {
            opt.selected = true;
            console.log(opt.value);

        }
    }
}
