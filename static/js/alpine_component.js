
document.addEventListener('alpine:init', () => {
    Alpine.data('sortList', (initialItems, saveUrl, csrfToken) => ({
        items: initialItems,
        async updateOrder(itemToMove, newIndex) {
            
            const itemList = initialItems;
            console.log("Original items:", itemList); 

            console.log("Replaced Item", itemToMove)
            const currentIndex = itemList.findIndex(item => JSON.stringify(item) === JSON.stringify(itemToMove));

            const newList = [...itemList];

            newList.splice(currentIndex, 1) //remove the item from the old position
            newList.splice(newIndex, 0, itemToMove) //insert to new postion
            console.log("Updated items:", newList);
           
            try {
                const response = await fetch(saveUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken
                    },
                    // body: JSON.stringify({ items: this.items })
                    body: JSON.stringify({items: newList})
                });

                // Check if the HTTP status is OK
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                // Parse the JSON body
                const data = await response.json();

                // Now check if your backend sends a `success` field
                if (data.success) {
                    console.log('Order saved successfully');
                } else {
                    throw new Error('Failed to save order');
                }

            } catch (error) {
                console.error('Error:', error);
            }
        }

    }));
});