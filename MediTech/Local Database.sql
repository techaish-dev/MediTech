// Connect to MongoDB
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("mydb");

  // Create collections
  dbo.createCollection("Price_Master", function(err, res) {
    if (err) throw err;
    console.log("Price_Master collection created!");
  });

  dbo.createCollection("Customer_Master", function(err, res) {
    if (err) throw err;
    console.log("Customer_Master collection created!");
  });

  dbo.createCollection("Service_Record", function(err, res) {
    if (err) throw err;
    console.log("Service_Record collection created!");
  });

  // Insert documents into the collections
  dbo.collection("Customer_Master").insertMany([
    { CustomerId: 1, CustomerName: 'Zahid Builder', Taxable: 'Y', Discountable: 'Y' },
    { CustomerId: 2, CustomerName: 'ATech Computer', Taxable: 'Y', Discountable: 'N' },
    { CustomerId: 3, CustomerName: 'Kabeer Electronic', Taxable: 'N', Discountable: 'Y' },
    { CustomerId: 4, CustomerName: 'New Gulf Air', Taxable: 'N', Discountable: 'N' }
  ], function(err, res) {
    if (err) throw err;
    console.log("Number of documents inserted into Customer_Master: " + res.insertedCount);
  });

  dbo.collection("Price_Master").insertMany([
    { ServiceCode: 1, ServiceName: 'Website Development', ServiceType: 'S', Price: 500, DiscountPer: 10, TaxPer: 5 },
    { ServiceCode: 2, ServiceName: 'Graphic Design', ServiceType: 'S', Price: 300, DiscountPer: 15, TaxPer: 8 },
    { ServiceCode: 3, ServiceName: 'Social Media Marketing', ServiceType: 'N', Price: 700, DiscountPer: 12, TaxPer: 6 },
    { ServiceCode: 4, ServiceName: 'Content Writing', ServiceType: 'N', Price: 400, DiscountPer: 10, TaxPer: 5 },
    { ServiceCode: 5, ServiceName: 'SEO Optimization', ServiceType: 'S', Price: 600, DiscountPer: 18, TaxPer: 7 },
    { ServiceCode: 6, ServiceName: 'Mobile App Development', ServiceType: 'S', Price: 900, DiscountPer: 20, TaxPer: 10 },
    { ServiceCode: 7, ServiceName: 'Video Production', ServiceType: 'S', Price: 800, DiscountPer: 17, TaxPer: 9 },
    { ServiceCode: 8, ServiceName: 'Data Analysis', ServiceType: 'N', Price: 750, DiscountPer: 13, TaxPer: 7 },
    { ServiceCode: 9, ServiceName: 'UI/UX Design', ServiceType: 'S', Price: 650, DiscountPer: 14, TaxPer: 6 },
    { ServiceCode: 10, ServiceName: 'Email Marketing', ServiceType: 'N', Price: 550, DiscountPer: 11, TaxPer: 5 },
    { ServiceCode: 11, ServiceName: 'Print Media Advertising', ServiceType: 'N', Price: 700, DiscountPer: 16, TaxPer: 8 },
    { ServiceCode: 12, ServiceName: 'Consultation Services', ServiceType: 'N', Price: 1000, DiscountPer: 20, TaxPer: 12 },
    { ServiceCode: 13, ServiceName: 'E-commerce Solutions', ServiceType: 'S', Price: 850, DiscountPer: 15, TaxPer: 7 },
    { ServiceCode: 14, ServiceName: 'Cybersecurity Audit', ServiceType: 'S', Price: 950, DiscountPer: 19, TaxPer: 10 }
    { ServiceCode: 15, ServiceName: 'CRM Implementation', ServiceType: 'S', Price: 1100, DiscountPer: 18, TaxPer: 11 }
  ], function(err, res) {
    if (err) throw err;
    console.log("Number of documents inserted into Price_Master: " + res.insertedCount);
  });

  db.close();
});
