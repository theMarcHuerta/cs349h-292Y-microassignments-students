__global__ void sortOfExp(int* inputExps, float* inputValues) {
    int threadId = blockIdx.x * blockDim.x + threadIdx.x;  // dont know if this counts as 3 loads?
    int expValue = inputExps[threadId];       // 1 int memory load
    float baseValue = inputValues[threadId];  // 1 float memory load
    float result = 1.0;
    for (int i=0; i<expValue; i++) {  // assume loop arithmetic is "free"
        result *= baseValue;
        if (i < 2) {  // assume this check is "free"
            result *= 2.0f ;// 1 arithmetic op
        } else {
            result *= 4.0f; // 1 arithmetic op
        }
        resultValues[threadId] = result;  // 1 float memory store
    }
}

/////////////////////////////////////////////////////////////// 
class RDDL33tify : public RDD {
    
    RDD parent;


    RDDL33tify(RDD parentRDD) {
       parent = parentRDD;
    }


    bool hasMoreElements() {






    }

    std::string next() {




        
    } 
};






class RDDGroupByFirstWord : public RDD {

    RDD parent;
    Dictionary<string, string> dict;

    public:
    RDDGroupByFirstWord(RDD parentRDD) {
        parent = parentRDD;
    }

    bool hasMoreElements() {




    }
    
    std::string next() {




    }
};

class RDDFilterLongWords : public RDD {

    RDD parent;

    public:
    RDDFilterLongWords(RDD parentRDD) {
        parent = parentRDD;
    }

    bool hasMoreElements() {



    }
    std::string next() {




    }
};