from agent import (GuardAgent,ClassificationAgent,DetailsAgent,AgentProtocol,RecommendationAgent,OrderTakingAgent)
import os

def main():
    guard_agent = GuardAgent()
    classification_agent=ClassificationAgent()
    recommendation_agent = RecommendationAgent('recommendation_objects/apriori_recommendations.json',
                                                    'recommendation_objects/popularity_recommendation.csv'
                                                    )
    
    agent_dict: dict[str, AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "order_taking_agent": OrderTakingAgent(recommendation_agent),
        "recommendation_agent": recommendation_agent
    }
    
    messages = []

    while True:
        # Clear console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Print all previous messages
        print("\n\nMessages so far:\n")
        for message in messages:
            print(f"{message['role']}: {message['content']}")

        # Get user input
        prompt = input("\nUser: ")
        messages.append({"role": "user", "content": prompt})

        # Get Guard Agent's response
        guard_agent_response = guard_agent.get_response(messages)
        
        # handle special decision
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            messages.append(guard_agent_response)
            continue                                                          # skip to next iteration

        # Get classification agent's responce
        classification_agent_response = classification_agent.get_response(messages)
        chosen_agent = classification_agent_response["memory"]["classification_decision"]
        print ("Chosen Agent: ", chosen_agent)

        # Get the chosen agent's response
        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages)
        
        messages.append(response)       
        
        
        

if __name__ == "__main__":
    main()
    
   
    
