C bugcheck_probe.f: counting lines for checking suspected bugs by running YREC
C (pyrec-map, Nov 2026). Copy into a scratch copy of yrec/src (never the clone),
C add CALL PROBE('<stem>#<n> path'|'<stem>#<n> cond',V1,V2) at each suspected
C path (V1, V2 REAL*8; the interface is implicit), and CALL PROBE_DUMP before
C main.f's final STOP. Counts go to $YREC_PROBE (default probe.log), and every
C 4194304 calls to $YREC_PROBE.counts, which survives a STOP elsewhere.
      MODULE PROBE_MOD
      IMPLICIT NONE
      INTEGER NPR
      PARAMETER (NPR=2048)
      INTEGER IPRU
      INTEGER*8 NTOT
      CHARACTER*48 PRNAME(NPR)
      INTEGER*8 PRCNT(NPR)
      REAL*8 PRMIN(NPR,2), PRMAX(NPR,2)
      LOGICAL PRUSED(NPR)
      DATA IPRU /0/, NTOT /0/, PRUSED /NPR*.FALSE./
      SAVE
      END MODULE PROBE_MOD
C PROBE(NAME,V1,V2): count a hit of the tagged path NAME (hashed), keep the
C range of two REAL*8 values; the first hit is written at once.
      SUBROUTINE PROBE(NAME,V1,V2)
      USE PROBE_MOD
      IMPLICIT NONE
      CHARACTER*(*) NAME
      REAL*8 V1,V2
      INTEGER I,K,H
      CHARACTER*256 FN
      IF(IPRU.EQ.0)THEN
         CALL GET_ENVIRONMENT_VARIABLE('YREC_PROBE',FN)
         IF(LEN_TRIM(FN).EQ.0) FN = 'probe.log'
         OPEN(NEWUNIT=IPRU,FILE=TRIM(FN),STATUS='REPLACE')
      ENDIF
      H = 7
      DO I = 1,LEN_TRIM(NAME)
         H = MOD(H*31 + ICHAR(NAME(I:I)), 1000003)
      END DO
      K = MOD(H,NPR) + 1
      DO I = 1,NPR
         IF(.NOT.PRUSED(K))THEN
            PRUSED(K) = .TRUE.
            PRNAME(K) = NAME
            PRCNT(K) = 0
            PRMIN(K,1) = V1
            PRMAX(K,1) = V1
            PRMIN(K,2) = V2
            PRMAX(K,2) = V2
            WRITE(IPRU,'(A,A,2(1X,ES14.6))')'FIRST ',NAME,V1,V2
            FLUSH(IPRU)
            EXIT
         ENDIF
         IF(PRNAME(K).EQ.NAME) EXIT
         K = MOD(K,NPR) + 1
      END DO
      PRCNT(K) = PRCNT(K) + 1
      PRMIN(K,1) = MIN(PRMIN(K,1),V1)
      PRMAX(K,1) = MAX(PRMAX(K,1),V1)
      PRMIN(K,2) = MIN(PRMIN(K,2),V2)
      PRMAX(K,2) = MAX(PRMAX(K,2),V2)
      NTOT = NTOT + 1
      IF(IAND(NTOT,4194303_8).EQ.0) CALL PROBE_SAVE
      RETURN
      END
C PROBE_DUMP: write every probe's count and ranges (called before STOP).
      SUBROUTINE PROBE_DUMP
      USE PROBE_MOD
      IMPLICIT NONE
      INTEGER I
      CHARACTER*256 FN
      IF(IPRU.EQ.0)THEN
         CALL GET_ENVIRONMENT_VARIABLE('YREC_PROBE',FN)
         IF(LEN_TRIM(FN).EQ.0) FN = 'probe.log'
         OPEN(NEWUNIT=IPRU,FILE=TRIM(FN),STATUS='REPLACE')
      ENDIF
      WRITE(IPRU,'(A)')'END name count v1min v1max v2min v2max'
      DO I = 1,NPR
         IF(PRUSED(I)) WRITE(IPRU,'(A,A,1X,I14,4(1X,ES14.6))')'COUNT ',
     *     PRNAME(I),PRCNT(I),PRMIN(I,1),PRMAX(I,1),PRMIN(I,2),PRMAX(I,2)
      END DO
      CLOSE(IPRU)
      RETURN
      END
C PROBE_SAVE: rewrite the counts so far to <probe file>.counts (survives a STOP).
      SUBROUTINE PROBE_SAVE
      USE PROBE_MOD
      IMPLICIT NONE
      INTEGER I,IU
      CHARACTER*256 FN
      CALL GET_ENVIRONMENT_VARIABLE('YREC_PROBE',FN)
      IF(LEN_TRIM(FN).EQ.0) FN = 'probe.log'
      OPEN(NEWUNIT=IU,FILE=TRIM(FN)//'.counts',STATUS='REPLACE')
      DO I = 1,NPR
         IF(PRUSED(I)) WRITE(IU,'(A,A,1X,I14,4(1X,ES14.6))')'COUNT ',
     *     PRNAME(I),PRCNT(I),PRMIN(I,1),PRMAX(I,1),PRMIN(I,2),PRMAX(I,2)
      END DO
      CLOSE(IU)
      RETURN
      END
