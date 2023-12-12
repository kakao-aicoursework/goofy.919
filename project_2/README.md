# 프로젝트 2단계 - Langchain Library 적용해보기

### [요구사항]
1단계에서 세팅한 기본 GPT 환경에 Langchain Library 를 적용하여, 카카오 API를 잘 설명하는 챗봇을 완성해보자

### [진행가이드]
1. 제공된 프롬프트 데이터 (project_data_카카오싱크.txt) 는 LLM library 에 적용한다
2. prompt engineering 기법을 활용해서 chatGPT api 에 해당 데이터를 적용한다
3. LLM + prompt engineering 은 Langchain Library 를 이용해서 구성한다
4. 여러 반복을 통해 카카오 싱크 api 사용법을 잘 설명해주는 챗봇을 완성한다

### [결과 예시]
```text
User : 카카오싱크 기능이 무엇이 있는지 설명해주세요
Assistance : 
- 간편 가입: 동의 화면에서 서비스 약관까지 한 번에 동의 받을 수 있습니다.
- 더 다양한 사용자 정보 활용: 서비스 회원 가입 시 필요한 다양한 사용자 정보를 제공받을 수 있습니다. 이름, 이메일, 전화번호, 연령대, 생일, 성별, 출생연도, 배송지 등 정보를 제공합니다.

```