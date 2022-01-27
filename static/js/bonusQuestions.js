// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
var size=15;
document.getElementById('table').style.fontSize=size.toString()+'px';
function getSortedItems(items, sortField, sortDirection) {
    if ((sortField==="VoteCount") || (sortField==="ViewNumber"))
    {
        if (sortDirection==="asc")
        {
         return items.sort((a, b) => parseInt(a[sortField]) - parseInt(b[sortField]))
        }
        else
        {
            return items.sort((a, b) => parseInt(b[sortField]) - parseInt(a[sortField]))
        }

    }
    if (sortDirection === "asc")
    {
        return items.sort((a, b) => a[sortField] > b[sortField] ? 1:-1)
    }
    else
    {
        return items.sort((a, b) => a[sortField] < b[sortField]? 1:-1)
    }

}

function getFilteredItems(items, filterValue) {
    let results = [];
    for (let i=0; i<items.length; i++) {
        if (filterValue[0] ==='!'){
            if (filterValue.includes('Description')){
                if (!items[i]['Description'].includes(filterValue.substr(13,filterValue.length))){

                    results.push(items[i])
                }
            }
            else if (!items[i]['Title'].includes(filterValue.substr(1,filterValue.length))){
                results.push(items[i])

            }
        }
        else if (filterValue.includes('Description')){
            if (items[i]['Description'].includes(filterValue.substr(12,filterValue.length))){
                results.push(items[i])
            }

        }
        else if (items[i]['Title'].includes(filterValue)){
            results.push(items[i])
        }

    }
    return results
}



function toggleTheme() {
    console.log("toggle theme")
    var element = document.body;
   element.classList.toggle("dark-mode")
}

function increaseFont() {
    if (size<=20) {
        size++
    }

    document.getElementById('table').style.fontSize=size.toString()+'px'
}

function decreaseFont() {
    if (size>=3) {
        size--
    }

    document.getElementById('table').style.fontSize=size.toString()+'px'
}