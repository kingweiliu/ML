#include "Job.h"


CLock::CLock(){
    ::InitializeCriticalSection(&m_sc);
}

CLock::~CLock(){
    ::DeleteCriticalSection(&m_sc);
}

void CLock::Lock(){
    ::EnterCriticalSection(&m_sc);
}
void CLock::UnLock(){
    ::LeaveCriticalSection(&m_sc);
}