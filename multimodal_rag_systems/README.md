How should we embed each type of content from PDF?
 * PDF with images
   * find the image in pdf
   * extract the image and upload into S3.
   * pass the image url to VLM and ask it to describe
   * get that text embedded and also save the url of the image in db
 * PDF with tables
   * find the tables in pdf
   * converting the tables to markdown [WRONG].
   * So, Convert it into dataframe and embed
 * PDF with header and footer
   * find the header and footer in pdf
   * embed the header and footer only once
 * PDF with scanned pages  (where text extraction is not possible)
   * find the image in pdf
   * extract the image and upload into S3.
   * pass the image url to VLM and ask it to describe
   * get that text embedded and also save the url of the image in db
 * PDF with graphs/charts
   * find the image in pdf
   * extract the image and upload into S3.
   * pass the image url to VLM and ask it to describe
   * get that text embedded and also save the url of the image in db
 * PDF with Multi column layout
   * have layout-aware tool to understand every page's layout
   * and extract the text and embed
 * PDF with legends
   * have layout-aware tool to understand every page's layout
   * and extract the text and embed
 * PDF with floorplan / periodic tables with color coded values
     * they are called spatial document
     * learn about dealing with this type of files
 * PDF with duplicate pages
     * compare the chunks and find out duplicates
 * PDF with maths/chemical formula
     * convert the entire to to image and use VLM
