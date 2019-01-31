#include <iostream>
#include <wels/codec_api.h>
#include <wels/codec_ver.h>

int main() {

    OpenH264Version version = WelsGetCodecVersion();
    std::cout << "OpenH264 version: " << version.uMajor << "."
                                      << version.uMinor << "."
                                      << version.uRevision << "."
                                      << version.uReserved
                                      << std::endl;

    ISVCEncoder* encoder = nullptr;
    int result = WelsCreateSVCEncoder(&encoder);
    if(result != 0 || !encoder) {
        std::cout << "Unable to create OpenH264 encoder" << std::endl;
        return 1;
    }

    ISVCDecoder *decoder = nullptr;
    result = WelsCreateDecoder(&decoder);
    if(result != 0 || !decoder) {
        std::cout << "Unable to create OpenH264 decoder" << std::endl;
        return 1;
    }

    WelsDestroySVCEncoder(encoder);
    WelsDestroyDecoder(decoder);
    return 0;
}
