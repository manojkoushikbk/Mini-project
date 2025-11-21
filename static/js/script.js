function calculateBill() {
    // Get customer details
    const customerName = document.getElementById('customer_name').value;
    const phone = document.getElementById('phone').value;
    const billNo = document.getElementById('bill_no').value;

    if (!customerName || !phone) {
        alert('Please enter customer name and phone number');
        return;
    }

    // Get all items with quantity > 0
    const items = {};
    document.querySelectorAll('#item_list input[type="number"]').forEach(input => {
        const quantity = parseInt(input.value);
        if (quantity > 0) {
            items[input.dataset.id] = quantity;
        }
    });

    if (Object.keys(items).length === 0) {
        alert('Please select at least one item');
        return;
    }

    // Send data to server
    fetch('/calculate_bill', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            customer_name: customerName,
            phone: phone,
            bill_no: billNo,
            items: items
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
            return;
        }
        
        // Generate bill text
        let billText = `Bill No: ${data.bill_no}\n`;
        billText += `Customer Name: ${data.customer_name}\n`;
        billText += `Phone: ${data.phone}\n`;
        billText += `Date: ${new Date().toLocaleString()}\n`;
        billText += '\n=========================\n\n';
        
        // Add items
        data.items.forEach(item => {
            billText += `${item.name}\n`;
            billText += `${item.qty} x ${(item.price / item.qty).toFixed(2)} = ${item.price.toFixed(2)} Rs\n`;
        });
        
        billText += '\n=========================\n\n';
        
        // Add taxes
        if (data.snacks_tax > 0) {
            billText += `Snacks Tax (5%): ${data.snacks_tax.toFixed(2)} Rs\n`;
        }
        if (data.grocery_tax > 0) {
            billText += `Grocery Tax (1%): ${data.grocery_tax.toFixed(2)} Rs\n`;
        }
        if (data.hygiene_tax > 0) {
            billText += `Hygiene Tax (10%): ${data.hygiene_tax.toFixed(2)} Rs\n`;
        }
        
        billText += `\nTotal Amount: ${data.total.toFixed(2)} Rs`;
        
        // Display bill
        document.getElementById('bill_text').value = billText;
        
        // Reset quantities
        document.querySelectorAll('#item_list input[type="number"]').forEach(input => {
            input.value = 0;
        });
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while calculating the bill');
    });
}