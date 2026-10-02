import { useState } from "react";
import { useEffect,useRef } from "react";
import "./styles/app.css"

export const Home = () =>  {

  const[inputValue,setInputvalue] = useState("");
  const[data,setData] = useState([]);
  const[isLoading,setIsLoading] = useState(false);

  const[isSidebarOpen,setIsSidebarOpen] = useState(false)

  const msgEndRef = useRef(null);

  useEffect(()=>{
    msgEndRef.current?.scrollIntoView({behavior:"smooth"})
  },[data,isLoading])

  const handleFormSubmit = () => {

    if(!inputValue || isLoading){
        return ;
    }
    getAiResponce(inputValue);
    setInputvalue("")
  }

  const handleKeyDown = (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    handleFormSubmit();
  }
};


const getAiResponce = async (query) => {
  setIsLoading(true);

  const assistantMessageId = Date.now();

  // Add user's message
  setData((prev) => [
    ...prev,
    {
      id: Date.now(),
      role: "user",
      content: query,
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);

  // Add ONE empty assistant message
  setData((prev) => [
    ...prev,
    {
      id: assistantMessageId,
      role: "assistant",
      content: "",
      streaming: true,
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    },
  ]);

  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: query,
      }),
    });

    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`);
    }

    if (!res.body) {
      throw new Error("Streaming is not supported by this response.");
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    let assistantAnswer = "";

    while (true) {
      const { done, value } = await reader.read();

      if (done) {
        break;
      }

      const chunk = decoder.decode(value, {
        stream: true,
      });

      console.log(
        "STREAM CHUNK:",
        JSON.stringify(chunk)
      );

      assistantAnswer += chunk;

      setData((prev) =>
        prev.map((message) =>
          message.id === assistantMessageId
            ? {
                ...message,
                content: assistantAnswer,
                streaming: true,
              }
            : message
        )
      );
    }

    // Finish the assistant message
    setData((prev) =>
      prev.map((message) =>
        message.id === assistantMessageId
          ? {
              ...message,
              content: assistantAnswer,
              streaming: false,
            }
          : message
      )
    );
  } catch (error) {
    console.error("CampusAI error:", error);

    setData((prev) =>
      prev.map((message) =>
        message.id === assistantMessageId
          ? {
              ...message,
              content:
                "Sorry, I couldn't connect to CampusAI right now. Please try again.",
              streaming: false,
            }
          : message
      )
    );
  } finally {
    setIsLoading(false);
  }
};
  return (
    <div className="app">

      {/* ================= SIDEBAR ================= */}

      <aside className={`sidebar ${isSidebarOpen?"sidebar-open":""}`}>

        <div className="brand">
          <div className="brand-logo">✦</div>

          <div>
            <h1>CampusAI</h1>
            <span>College Assistant</span>
          </div>
        </div>

        <button
          className="new-chat-button"
          onClick={() => {
            setData([]);
            setInputvalue("");
            setIsSidebarOpen(false);
          }}
        >
          <span>＋</span>
          New chat
        </button>

        <div className="sidebar-bottom">

          <div className="profile">

            <div className="avatar">H</div>

            <div className="profile-info">
              <strong>Student</strong>
              <span>CampusAI account</span>
            </div>

            <span className="more">•••</span>

          </div>

        </div>

      </aside>

      {isSidebarOpen && (
          <div
            className="sidebar-overlay"
            onClick={() => setIsSidebarOpen(false)}
          />
        )}


      {/* ================= MAIN ================= */}

      <main className="main">

        {/* HEADER */}

        <header className="header">

          <div className="mobile-brand">

            <button className="mobile-menu-button" onClick={()=>setIsSidebarOpen(true)} >
              ☰
            </button>

            <div className="brand-logo">
              ✦
            </div>

            <strong>
              CampusAI
            </strong>

          </div>

          <div className="header-actions">
            <h2> CampusAI</h2>

          </div>

        </header>


        {/* ================= CONVERSATION ================= */}

        <section className="conversation">

          <div className="messages">
                    {data.length === 0 && !isLoading && (
                    <div className="welcome">

                      <div className="welcome-logo">
                        ✦
                      </div>

                      <h1>
                        Welcome to CampusAI
                      </h1>

                      <p>
                        Your intelligent college assistant
                      </p>

                      <span className="welcome-description">
                        Ask questions about your college documents,
                        rules, exams, hostel and campus procedures.
                      </span>

                      <div className="suggestions">

                        <button
                          onClick={() =>
                            setInputvalue("What are the hostel rules?")
                          }
                        >
                          🏠
                          <span>Hostel rules</span>
                        </button>

                        <button
                          onClick={() =>
                            setInputvalue("What is the outpass procedure?")
                          }
                        >
                          🎫
                          <span>Outpass procedure</span>
                        </button>

                        <button
                          onClick={() =>
                            setInputvalue("What documents are required for exams?")
                          }
                        >
                          📚
                          <span>Exam information</span>
                        </button>

                        <button
                          onClick={() =>
                            setInputvalue("What are the campus rules?")
                          }
                        >
                          🏫
                          <span>Campus rules</span>
                        </button>

                      </div>

                    </div>
                  )}
            {data.map((message,index) => (

              <div
                key={index}
                className={`message-row ${message.role}`}
              >

                {message.role === "assistant" && (
                  <div className="message-avatar ai-avatar">
                    ✦
                  </div>
                )}

                <div className="message-content">

                  <div className="message-header">
                    <span className="message-name">
                      {message.role === "user"
                        ? "You"
                        : "CampusAI"}
                    </span>

                    <span className="message-time">
                      {message.time}
                    </span>

                  </div>


                  {message.streaming && !message.content ? (
  <div className="thinking-indicator">
    <span className="thinking-dot"></span>
    <span className="thinking-dot"></span>
    <span className="thinking-dot"></span>
  </div>
) : (
  <div className="message-text">

    {message.content
      .split("\n")
      .map((line, index) => {

        const trimmedLine = line.trim();

        if (trimmedLine.startsWith("-")) {
          return (
            <div
              key={index}
              className="answer-point"
            >
              <span className="bullet">
                •
              </span>

              <span>
                {trimmedLine.substring(1).trim()}
              </span>
            </div>
          );
        }

        if (trimmedLine === "") {
          return (
            <div
              key={index}
              className="answer-space"
            />
          );
        }

        return (
          <div
            key={index}
            className="answer-text-line"
          >
            {trimmedLine}
          </div>
        );
      })}

  </div>
)}
                  {message.sources && message.sources.length > 0 && (

  <div className="sources-container">

    {message.sources.map((source, sourceIndex) => (

      <div
        className="source-card"
        key={sourceIndex}
      >

        <div className="source-icon">
          📄
        </div>

        <div className="source-info">

          <strong>
            {source.file.split("/").pop()}
          </strong>

          <span>
            Page {source.page}
          </span>

        </div>

        <span className="source-arrow">
          ↗
        </span>

      </div>

    ))}

  </div>

)}
                </div>

              </div>

            ))}


            <div ref={msgEndRef} />

          </div>


          {/* ================= INPUT ================= */}

          <div className="input-wrapper">

            <div className="input-box">

              <button className="attach-button">
                ＋
              </button>

              <textarea
                  type="text"
                  placeholder="Ask a follow-up..."
                  value={inputValue}
                  onChange={(e)=>{setInputvalue(e.target.value);e.target.style.height="auto";e.target.style.height=`${Math.min(e.target.scrollHeight,120)}px`}}
                  onKeyDown={handleKeyDown}
                  rows={1}

              />

              <div className="input-actions">

                <button className="mic-button">
                  ⌁
                </button>

                <button className="send-button" onClick={handleFormSubmit} disabled={!inputValue.trim() || isLoading} >
                  ↑
                </button>

              </div>

            </div>

            <p className="disclaimer">
              CampusAI can make mistakes. Always verify important
              information with official college sources.
            </p>

          </div>

        </section>

      </main>

    </div>
  );
}
