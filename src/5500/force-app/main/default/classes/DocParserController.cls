public class DocParserController {
    
    public static void processDocument(String publicUrl) {
        // Step 1: Fetch the file from the public URL
        Blob pdfBlob = fetchFileFromUrl(publicUrl);
        
        // Step 2: Upload the Document to DocParser
        uploadToDocParser(pdfBlob);
        
        // Step 3: List the documents to get their IDs
        List<String> documentIds = listDocumentIds();
        
        // Step 4: Apply Parsing Rules via API
        for(String docId : documentIds) {
            if(docId == documentIds[0]) {
                // First 3 pages
                applyParsingRule(docId, 'parser_id_for_first_3_pages');
            } else {
                // Other 4-page sections
                applyParsingRule(docId, 'parser_id_for_other_sections');
            }
            
            // Step 5: Extract the JSON for Each Parsed File from DocParser
            String parsedJson = extractParsedJson(docId);
            
            // Further processing of parsedJson
        }
    }
    
    public static Blob fetchFileFromUrl(String publicUrl) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint(publicUrl);
        req.setMethod('GET');
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        return res.getBodyAsBlob();
    }
    
    public static String uploadToDocParser(Blob pdfBlob) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:DocParser_Named_Credential/v1/document/upload');
        req.setMethod('POST');
        req.setHeader('Authorization', 'Bearer YOUR_API_KEY');
        req.setBodyAsBlob(pdfBlob);
        req.setHeader('Content-Type', 'application/pdf');
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        return res.getBody();
    }

    public static List<String> listDocumentIds() {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:DocParser_Named_Credential/v1/document/list');
        req.setMethod('GET');
        req.setHeader('Authorization', 'Bearer YOUR_API_KEY');
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        // Logic to extract multiple document IDs from the list response
        return new List<String>{'doc_id_1', 'doc_id_2', 'doc_id_3'}; // Replace with actual extracted IDs
    }
    
    public static List<String> extractDocumentIds(String uploadResponse) {
        // Logic to extract multiple document IDs from the upload response
        return new List<String>{'doc_id_1', 'doc_id_2', 'doc_id_3'}; // Replace with actual extracted IDs
    }
    
    public static void applyParsingRule(String documentId, String parserId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:DocParser_Named_Credential/v1/document/parse/' + documentId);
        req.setMethod('POST');
        req.setHeader('Authorization', 'Bearer YOUR_API_KEY');
        req.setBody('{"parser_id": "' + parserId + '"}');
        
        Http http = new Http();
        HttpResponse res = http.send(req);
    }
    
    public static String extractParsedJson(String documentId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:DocParser_Named_Credential/v1/results/' + documentId);
        req.setMethod('GET');
        req.setHeader('Authorization', 'Bearer YOUR_API_KEY');
        
        Http http = new Http();
        HttpResponse res = http.send(req);
        
        return res.getBody();
    }
}
