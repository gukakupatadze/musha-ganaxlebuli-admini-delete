export const translations = {
  ka: {
    // Header
    home: "მთავარი",
    services: "სერვისები",
    about: "ჩვენ შესახებ",
    contact: "კონტაქტი",
    caseTracking: "საქმის თვალთვალი",
    
    // Hero Section
    heroTitle: "მონაცემთა აღდგენის პროფესიონალები",
    heroSubtitle: "DataLab Georgia - საქართველოს წამყვანი მონაცემთა აღდგენის სერვისი. ჩვენ ვაღვადგენთ თქვენს მნიშვნელოვან ინფორმაციას ნებისმიერი მოწყობილობიდან.",
    getStarted: "დაიწყეთ ახლავე",
    freeConsultation: "უფასო კონსულტაცია",
    
    // Services
    servicesTitle: "ჩვენი სერვისები",
    servicesSubtitle: "თანამედროვე ტექნოლოგიებითა და გამოცდილი სპეციალისტებით ვაღვადგენთ მონაცემებს",
    
    dataRecovery: "HDD აღდგენა",
    dataRecoveryDesc: "დაზიანებული მყარი დისკებიდან ფაილების აღდგენა",
    
    dataBackup: "SSD აღდგენა",
    dataBackupDesc: "დაზიანებული SSD დისკებიდან ფაილების აღდგენა",
    
    hardwareRepair: "USB აღდგენა",
    hardwareRepairDesc: "USB ,SD, microSD ბარათებიდან მონაცემთა აღდგენა",
    
    forensicRecovery: "RAID აღდგენა",
    forensicRecoveryDesc: "RAID მასივებიდან მონაცემთა აღდგენა და კონფიგურაციები",
    
    // Service Request
    serviceRequestTitle: "სერვისის მოთხოვნა",
    serviceRequestSubtitle: "მოგვწერეთ თქვენი პრობლემის შესახებ და მიიღეთ პროფესიონალური რჩევა",
    
    // Price Estimation
    priceEstimationTitle: "ფასის გაანგარიშება",
    priceEstimationSubtitle: "მიიღეთ წინასწარი ფასის შეფასება",
    
    // Case Tracking
    caseTrackingTitle: "საქმის თვალთვალი",
    caseTrackingSubtitle: "შეამოწმეთ თქვენი საქმის სტატუსი",
    
    // Testimonials
    testimonialsTitle: "მომხმარებელთა გამოხმაურება",
    testimonialsSubtitle: "რას ამბობენ ჩვენი კმაყოფილი კლიენტები",
    
    // Contact
    contactTitle: "დაგვიკავშირდით",
    contactSubtitle: "მზად ვართ გაგეხმაროთ 24/7",
    
    // Footer
    footerDesc: "DataLab Georgia - საქართველოს საიმედო მონაცემთა აღდგენის სერვისი",
    quickLinks: "სწრაფი ლინკები",
    contactInfo: "საკონტაქტო ინფორმაცია",
    allRightsReserved: "ყველა უფლება დაცულია"
  },
  
  en: {
    // Header
    home: "Home",
    services: "Services",
    about: "About",
    contact: "Contact",
    caseTracking: "Case Tracking",
    
    // Hero Section
    heroTitle: "Data Recovery Professionals",
    heroSubtitle: "DataLab Georgia - Georgia's leading data recovery service. We restore your important information from any device.",
    getStarted: "Get Started",
    freeConsultation: "Free Consultation",
    
    // Services
    servicesTitle: "Our Services",
    servicesSubtitle: "We recover data using modern technologies and experienced specialists",
    
    dataRecovery: "HDD Recovery",
    dataRecoveryDesc: "File recovery from damaged hard drives",
    
    dataBackup: "SSD Recovery",
    dataBackupDesc: "File recovery from damaged SSD drives",
    
    hardwareRepair: "USB Recovery",
    hardwareRepairDesc: "Data recovery from USB, SD, microSD cards",
    
    forensicRecovery: "RAID Recovery",
    forensicRecoveryDesc: "Data recovery from RAID arrays and configurations",
    
    // Service Request
    serviceRequestTitle: "Service Request",
    serviceRequestSubtitle: "Tell us about your problem and get professional advice",
    
    // Price Estimation
    priceEstimationTitle: "Price Estimation",
    priceEstimationSubtitle: "Get a preliminary price assessment",
    
    // Case Tracking
    caseTrackingTitle: "Case Tracking",
    caseTrackingSubtitle: "Check the status of your case",
    
    // Testimonials
    testimonialsTitle: "Customer Testimonials",
    testimonialsSubtitle: "What our satisfied clients say",
    
    // Contact
    contactTitle: "Contact Us",
    contactSubtitle: "We're ready to help you 24/7",
    
    // Footer
    footerDesc: "DataLab Georgia - Georgia's reliable data recovery service",
    quickLinks: "Quick Links",
    contactInfo: "Contact Information",
    allRightsReserved: "All rights reserved"
  }
};

// Mock data for services
export const services = [
  {
    id: 1,
    icon: "HardDrive",
    titleKey: "dataRecovery",
    descKey: "dataRecoveryDesc",
    features: ["მექანიკური დაზიანება", "ლოგიკური შეცდომა", "ფაილების წაშლა", "დისკი არ იკითხება"],
    price: "150₾ დან"
  },
  {
    id: 2,
    icon: "Zap",
    titleKey: "dataBackup",
    descKey: "dataBackupDesc",
    features: ["კონტროლერის დაზიანება", "Flash მეხსიერების ცვეთა", "Firmware კორუფცია", "NAND ჩიპები"],
    price: "200₾ დან"
  },
  {
    id: 3,
    icon: "Usb",
    titleKey: "hardwareRepair",
    descKey: "hardwareRepairDesc",
    features: ["ფიზიკური დაზიანება", "კონტროლერის პრობლემები", "ფორმატირების შემდეგ", "NAND ჩიპები"],
    price: "დან 150₾"
  },
  {
    id: 4,
    icon: "Search",
    titleKey: "forensicRecovery",
    descKey: "forensicRecoveryDesc",
    features: ["Legal Documentation", "Chain of Custody", "Expert Testimony", "Court Admissible"],
    price: "დან 300₾"
  }
];

// Mock data removed - now using API endpoints