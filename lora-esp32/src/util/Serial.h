// initializer
void initSerial();
// main struct to use when sending serial data
struct jsonObject {
    // what message ID
    int ID;
    // normal message content
    String msg;
    /*
        @TODO: add all the stuff we need here
    */ 
};
// standard caller functions
void srlError(String type, String errorMsg);
void srlInfo(String type, String infoMsg);
// reciever loop
void srlRX();

