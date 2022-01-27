// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {
    console.log(items)
    console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    // for (let i=0; i<filterValue.length; i++) {
    //     items.pop()
    // }
    function checkForValue(element) {
        return filterValue in element;
}

    filtered_items = items.filter(checkForValue)
    return filtered_items
}



function toggleTheme() {
    console.log("toggle theme")
    var element = document.body;
   element.classList.toggle("dark-mode")
}

var min = 10;
var max = 25;

function changeFontSize(delta) {
  var tags = document.querySelectorAll('input, table, button');
  for (i = 0; i < tags.length; i++) {
    if (tags[i].style.fontSize) {
      var s = parseInt(tags[i].style.fontSize.replace("px", ""));
    } else {
      var s = 17;
    } if (s != max) {
      s += delta;
    }
    tags[i].style.fontSize = s + "px"
  }
}

function increaseFont() {
    changeFontSize(1);
    console.log("increaseFont");
}

function decreaseFont() {
    console.log("decreaseFont");
    changeFontSize((-1));
}