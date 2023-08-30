import { LightningElement, track } from 'lwc';
const jsonData = [
    {
        "id": "225731f525f475a4e11de17d8569cf0e",
        "document_id": "d69a8ced99d0f4e8c89bbad970fa506a",
        "remote_id": "",
        "file_name": "Dropbox 5500.pdf",
        "media_link": "https://api.docparser.com/v1/document/media/C8PJLzUJ_FlI2ZqGSM0u-k7Z-kLaIyLzMvwlwgnKwajSSB1gOjmE_4WCL5FeO8AxqBe9epqzxow1nWlwh9djYUYS9tp79XJ3da5IoLMFpYc",
        "media_link_original": "https://api.docparser.com/v1/document/media/C8PJLzUJ_FlI2ZqGSM0u-k7Z-kLaIyLzMvwlwgnKwajSSB1gOjmE_4WCL5FeO8AxqBe9epqzxow1nWlwh9djYUYS9tp79XJ3da5IoLMFpYc/original",
        "media_link_data": "https://api.docparser.com/v1/document/media/C8PJLzUJ_FlI2ZqGSM0u-k7Z-kLaIyLzMvwlwgnKwajSSB1gOjmE_4WCL5FeO8AxqBe9epqzxow1nWlwh9djYUYS9tp79XJ3da5IoLMFpYc/data",
        "page_count": 27,
        "uploaded_at": "2023-08-27T20:02:50+00:00",
        "processed_at": "2023-08-27T20:02:52+00:00",
        "uploaded_at_utc": "2023-08-27T20:02:50+00:00",
        "uploaded_at_user": "2023-08-27T12:02:50+00:00",
        "processed_at_utc": "2023-08-27T20:02:52+00:00",
        "processed_at_user": "2023-08-27T12:02:52+00:00",
        "basic_plan_information__name_of_plan": "DROPBOX, INC. HEALTH AND WELFARE PLAN",
        "basic_plan_information__plan_sponsors_name": "DROPBOX, INC",
        "basic_plan_information__plan_sponsors_addresss": "333 BRANNAN STREET\nSAN FRANCISCO, CA 94107",
        "annual_report_identification_information__a_single_employer_plan": {
            "value": "Yes",
            "confidence": 72
        },
        "annual_report_identification_information__a_multiemployer_plan": {
            "value": "No",
            "confidence": 0
        },
        "annual_report_identification_information__an_amended_returnreport": {
            "value": "No",
            "confidence": 0
        },
        "annual_report_identification_information__first_returnreport": {
            "value": "No",
            "confidence": 0
        },
        "annual_report_identification_information__form_5558": {
            "value": 1,
            "confidence": 20
        },
        "annual_report_identification_information__special_extension": {
            "value": "False",
            "confidence": 0
        },
        "annual_report_identification_information__funding_arrangement_code_section_412e3_insurance_contracts": {
            "value": "False",
            "confidence": 20
        },
        "annual_report_identification_information__funding_arrangement_trust": {
            "value": "False",
            "confidence": 0
        },
        "annual_report_identification_information__funding_arrangement_general_assets_of_the_sponser": {
            "value": "True",
            "confidence": 20
        },
        "annual_report_identification_information__funding_arrangement_insurance": {
            "value": 1,
            "confidence": 20
        },
        "annual_report_identification_information__multiple_employer_plan": {
            "value": 0,
            "confidence": 20
        },
        "annual_report_identification_information__the_final_returnreport": {
            "value": 0,
            "confidence": 0
        },
        "annual_report_identification_information__dfe": {
            "value": 0,
            "confidence": 20
        },
        "annual_report_identification_information__a_short_plan_year": {
            "value": 0,
            "confidence": 20
        },
        "annual_report_identification_information__automatic_extension": {
            "value": 0,
            "confidence": 20
        },
        "annual_report_identification_information__collectively_bargained": {
            "value": 1,
            "confidence": 20
        },
        "annual_report_identification_information__dvfc": {
            "value": 0,
            "confidence": 20
        },
        "calendar_year": "2018",
        "annual_report_identification_information__plan_number": "501\n001",
        "annual_report_identification_information__effective_start_date": "11/01/2012",
        "annual_report_identification_information__plan_sponsors_telephone_number": "26-0138832",
        "annual_report_identification_information__ein": "mber\n415-986-7057\n23456789",
        "annual_report_identification_information__business_code": "443142\n012345",
        "signature_of_plan_administrator__signature": "Filed with authorized/valid electronic signature.",
        "signature_of_plan_administrator__name" : "MEGAN\nWEBBER\nABCDEFGHI\nABCDEFGHI\n\nABCDEFGHI A",
        "signature_of_plan_administrator__date": "10/05/2019",
        "signature_of_plan_sponsor__signature": "Filed with authorized/valid electronic signature.",
        "signature_of_plan_sponsor__date": "10/05/2019",
        "signature_of_plan_sponsor__name": "MEGAN\nWEBBER"
    }
];

export default class JsonTable extends LightningElement {
    @track sections = [];

    connectedCallback() {
        this.sections = this.createTableSections(jsonData[0]);
    }

    castToTrueString(value) {
        if (value === 1 || value === "Yes" || value === "True" || value === true) {
            return "true";
        }
        return "false";
    }

    createTableSections(data) {
        const sectionMap = {};

        Object.keys(data).forEach(key => {
            const [sectionName, fieldName] = key.split('__');
            const sectionKey = sectionName || 'Unnamed Section';

            if (!sectionMap[sectionKey]) {
                sectionMap[sectionKey] = { name: sectionName, fields: [] };
            }

            let value = data[key];

            if (typeof value === 'object' && value !== null && 'value' in value) {
                value = this.castToTrueString(value.value);
            }

            sectionMap[sectionKey].fields.push({
                key: fieldName || key,
                name: fieldName || key,
                value: value === "true" ? true : value === "false" ? false : value,
                isBoolean: value === 'true' || value === 'false'
            });

        });

        return Object.keys(sectionMap).map(key => ({
            key,
            name: sectionMap[key].name || key,
            fields: sectionMap[key].fields
        }));
    }
}